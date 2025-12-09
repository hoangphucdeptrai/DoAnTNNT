from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

# File lưu dữ liệu thực tế
DATA_FILE = 'data.csv'

# Khởi tạo dữ liệu mẫu nếu chưa có file (để tránh lỗi khi chạy lần đầu)
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame({
        'word_count': [300, 500, 1000],
        'image_count': [1, 2, 5],
        'load_time': [1.0, 1.5, 2.0],
        'is_desktop': [0, 1, 1],
        'time_on_page': [20, 45, 90] # Giả định ban đầu
    })
    df_init.to_csv(DATA_FILE, index=False)

# Hàm huấn luyện lại model từ file CSV
def train_model():
    df = pd.read_csv(DATA_FILE)
    # Nếu dữ liệu quá ít thì chưa train
    if len(df) < 5:
        return None, 0
    
    X = df[['word_count', 'image_count', 'load_time', 'is_desktop']]
    y = df['time_on_page']
    
    model = LinearRegression()
    model.fit(X, y)
    return model, len(df)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Nhận thông số trang web từ Client để dự đoán
    data = request.json
    model, data_count = train_model()
    
    # Tính thời gian trung bình từ dữ liệu thực tế
    df = pd.read_csv(DATA_FILE)
    avg_time = round(df['time_on_page'].mean(), 2)
    min_time = round(df['time_on_page'].min(), 2)
    max_time = round(df['time_on_page'].max(), 2)
    
    if model:
        # Dự đoán thời gian dựa trên dữ liệu hiện có
        features = [[data['word_count'], data['image_count'], data['load_time'], data['is_desktop']]]
        prediction = model.predict(features)[0]
    else:
        prediction = 30 # Giá trị mặc định nếu chưa đủ dữ liệu train
        
    return jsonify({
        'prediction': round(prediction, 2),
        'data_count': data_count,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time
    })

@app.route('/save_data', methods=['POST'])
def save_data():
    # Nhận thời gian thực tế người dùng đã xem và lưu lại
    data = request.json
    new_row = pd.DataFrame([data])
    
    # Lưu nối tiếp vào file CSV (mode='a')
    new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
    
    print(f"--> Đã lưu dữ liệu mới: User ở lại {data['time_on_page']}s")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)