from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
import json
from ml_model import TimePredictor

app = Flask(__name__)

# Khởi tạo AI Model
predictor = TimePredictor()

# File lưu dữ liệu tracking
TRACKING_FILE = 'tracking_data.csv'

# Khởi tạo file tracking nếu chưa có
if not os.path.exists(TRACKING_FILE):
    df_init = pd.DataFrame({
        'product_id': [],
        'page_type': [],
        'time_on_page': [],
        'device_type': [],
        'timestamp': []
    })
    df_init.to_csv(TRACKING_FILE, index=False)

# Dữ liệu sản phẩm mẫu
PRODUCTS = [
    {
        'id': 1,
        'name': 'Áo Thun Nam Basic',
        'category': 'Quần Áo',
        'price': 199000,
        'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
        'description': 'Áo thun nam chất liệu cotton 100%, thoáng mát, form regular fit',
        'rating': 4.5,
        'sold': 1234
    },
    {
        'id': 2,
        'name': 'Quần Jean Slim Fit',
        'category': 'Quần Áo',
        'price': 450000,
        'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
        'description': 'Quần jean nam form slim fit, chất liệu denim cao cấp',
        'rating': 4.8,
        'sold': 856
    },
    {
        'id': 3,
        'name': 'Giày Sneaker Trắng',
        'category': 'Giày Dép',
        'price': 599000,
        'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
        'description': 'Giày sneaker trắng basic, phù hợp mọi phong cách',
        'rating': 4.7,
        'sold': 2341
    },
    {
        'id': 4,
        'name': 'Balo Laptop 15.6 inch',
        'category': 'Phụ Kiện',
        'price': 350000,
        'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
        'description': 'Balo laptop chống nước, nhiều ngăn tiện dụng',
        'rating': 4.6,
        'sold': 678
    },
    {
        'id': 5,
        'name': 'Đồng Hồ Nam Thời Trang',
        'category': 'Phụ Kiện',
        'price': 890000,
        'image': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=400',
        'description': 'Đồng hồ nam dây da, mặt kính sapphire chống xước',
        'rating': 4.9,
        'sold': 445
    },
    {
        'id': 6,
        'name': 'Áo Khoác Hoodie',
        'category': 'Quần Áo',
        'price': 399000,
        'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
        'description': 'Áo hoodie unisex, chất nỉ bông mềm mại ấm áp',
        'rating': 4.4,
        'sold': 1567
    }
]

CATEGORIES = ['Tất Cả', 'Quần Áo', 'Giày Dép', 'Phụ Kiện']

@app.route('/')
def home():
    return render_template('home.html', products=PRODUCTS, categories=CATEGORIES)

@app.route('/products')
def products():
    category = request.args.get('category', 'Tất Cả')
    if category == 'Tất Cả':
        filtered_products = PRODUCTS
    else:
        filtered_products = [p for p in PRODUCTS if p['category'] == category]
    return render_template('products.html', products=filtered_products, categories=CATEGORIES, selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return "Sản phẩm không tồn tại", 404

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin/model')
def admin_model():
    """Trang hiển thị thông tin Model AI"""
    predictor.train()
    model_info = predictor.get_model_info()
    importance = predictor.get_feature_importance()
    
    return render_template('model_info.html', 
                         model_info=model_info, 
                         importance=importance)

@app.route('/admin/analytics')
def admin_analytics():
    if not os.path.exists(TRACKING_FILE):
        return render_template('analytics.html', stats={})
    
    df = pd.read_csv(TRACKING_FILE)
    
    if len(df) == 0:
        return render_template('analytics.html', stats={})
    
    # Thống kê theo loại trang
    page_stats = df.groupby('page_type').agg({
        'time_on_page': ['mean', 'count', 'sum', 'min', 'max']
    }).round(2)
    page_stats.columns = ['avg_time', 'visits', 'total_time', 'min_time', 'max_time']
    page_stats = page_stats.to_dict('index')
    
    # Thống kê theo sản phẩm
    product_df = df[df['product_id'] > 0]
    if len(product_df) > 0:
        product_stats = product_df.groupby('product_id').agg({
            'time_on_page': ['mean', 'count', 'sum']
        }).round(2)
        product_stats.columns = ['avg_time', 'visits', 'total_time']
        product_stats = product_stats.to_dict('index')
        
        # Thêm tên sản phẩm
        for pid in product_stats:
            product = next((p for p in PRODUCTS if p['id'] == pid), None)
            if product:
                product_stats[pid]['name'] = product['name']
                product_stats[pid]['category'] = product['category']
    else:
        product_stats = {}
    
    # Thống kê theo thiết bị
    device_stats = df.groupby('device_type').agg({
        'time_on_page': ['mean', 'count']
    }).round(2)
    device_stats.columns = ['avg_time', 'visits']
    device_stats = device_stats.to_dict('index')
    
    stats = {
        'total_visits': len(df),
        'total_time': round(df['time_on_page'].sum(), 2),
        'overall_avg': round(df['time_on_page'].mean(), 2),
        'page_stats': page_stats,
        'product_stats': product_stats,
        'device_stats': device_stats
    }
    
    return render_template('analytics.html', stats=stats)

# API tracking thời gian xem trang
@app.route('/api/track', methods=['POST'])
def track_time():
    data = request.json
    new_row = pd.DataFrame([{
        'product_id': data.get('product_id', 0),
        'page_type': data.get('page_type', 'home'),
        'time_on_page': data['time_on_page'],
        'device_type': data.get('device_type', 'desktop'),
        'timestamp': pd.Timestamp.now()
    }])
    new_row.to_csv(TRACKING_FILE, mode='a', header=False, index=False)
    print(f"📊 Tracked: {data['page_type']} - {data['time_on_page']}s")
    return jsonify({'status': 'success'})

# API lấy thống kê
@app.route('/api/stats')
def get_stats():
    if os.path.exists(TRACKING_FILE):
        df = pd.read_csv(TRACKING_FILE)
        if len(df) > 0:
            stats = {
                'total_visits': len(df),
                'avg_time': round(df['time_on_page'].mean(), 2),
                'total_time': round(df['time_on_page'].sum(), 2)
            }
            return jsonify(stats)
    return jsonify({'total_visits': 0, 'avg_time': 0, 'total_time': 0})

# API dự đoán thời gian xem
@app.route('/api/predict', methods=['POST'])
def predict_time():
    data = request.json
    product_id = data.get('product_id', 0)
    device_type = data.get('device_type', 'desktop')
    
    # Train model nếu chưa train
    if not predictor.is_trained:
        predictor.train()
    
    # Dự đoán
    prediction = predictor.predict(product_id, device_type)
    
    return jsonify({
        'predicted_time': prediction,
        'model_trained': predictor.is_trained
    })

# API thông tin model
@app.route('/api/model-info')
def model_info():
    predictor.train()  # Retrain với data mới nhất
    info = predictor.get_model_info()
    importance = predictor.get_feature_importance()
    
    if info:
        info['feature_importance'] = importance
        return jsonify(info)
    return jsonify({'error': 'Model chưa được train'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
