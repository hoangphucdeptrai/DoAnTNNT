"""
Script tạo dữ liệu giả lập để train AI model
80% dữ liệu giả + 20% dữ liệu thực từ người dùng
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_samples=200):
    """
    Tạo dữ liệu giả lập dựa trên logic thực tế:
    - Sản phẩm có giá cao thường được xem lâu hơn
    - Desktop xem lâu hơn Mobile
    - Sản phẩm hot (rating cao) được xem lâu hơn
    """
    
    # Thông tin sản phẩm (từ app_shop.py)
    products = [
        {'id': 1, 'price': 199000, 'rating': 4.5, 'category': 'Quần Áo'},
        {'id': 2, 'price': 450000, 'rating': 4.8, 'category': 'Quần Áo'},
        {'id': 3, 'price': 599000, 'rating': 4.7, 'category': 'Giày Dép'},
        {'id': 4, 'price': 350000, 'rating': 4.6, 'category': 'Phụ Kiện'},
        {'id': 5, 'price': 890000, 'rating': 4.9, 'category': 'Phụ Kiện'},
        {'id': 6, 'price': 399000, 'rating': 4.4, 'category': 'Quần Áo'},
    ]
    
    data = []
    
    for _ in range(num_samples):
        # Chọn ngẫu nhiên sản phẩm
        product = random.choice(products)
        
        # Chọn loại trang
        page_types = ['home', 'products', 'product_detail', 'contact']
        weights = [0.3, 0.25, 0.4, 0.05]  # product_detail có tỷ lệ cao nhất
        page_type = random.choices(page_types, weights=weights)[0]
        
        # Chọn thiết bị (60% desktop, 40% mobile)
        device_type = random.choices(['desktop', 'mobile'], weights=[0.6, 0.4])[0]
        
        # Tính thời gian xem dựa trên logic thực tế
        base_time = 15  # Thời gian cơ bản
        
        # Điều chỉnh theo loại trang
        if page_type == 'home':
            base_time = random.uniform(10, 30)
        elif page_type == 'products':
            base_time = random.uniform(15, 45)
        elif page_type == 'product_detail':
            base_time = random.uniform(20, 90)
            # Sản phẩm giá cao được xem lâu hơn
            if product['price'] > 500000:
                base_time *= 1.3
            # Rating cao được xem lâu hơn
            if product['rating'] >= 4.7:
                base_time *= 1.2
        else:  # contact
            base_time = random.uniform(5, 20)
        
        # Desktop xem lâu hơn mobile 20-30%
        if device_type == 'desktop':
            base_time *= random.uniform(1.2, 1.3)
        
        # Thêm noise ngẫu nhiên
        time_on_page = base_time * random.uniform(0.8, 1.2)
        
        # Tạo timestamp ngẫu nhiên trong 30 ngày qua
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago, 
                                               hours=random.randint(0, 23),
                                               minutes=random.randint(0, 59))
        
        data.append({
            'product_id': product['id'] if page_type == 'product_detail' else 0,
            'page_type': page_type,
            'time_on_page': round(time_on_page, 3),
            'device_type': device_type,
            'timestamp': timestamp
        })
    
    return pd.DataFrame(data)

def initialize_tracking_data():
    """Khởi tạo file tracking_data.csv với dữ liệu giả lập"""
    
    print("🤖 Đang tạo dữ liệu giả lập để train AI...")
    
    # Tạo 200 mẫu dữ liệu giả (80% của 250 mẫu dự kiến)
    df = generate_synthetic_data(num_samples=200)
    
    # Sắp xếp theo thời gian
    df = df.sort_values('timestamp')
    
    # Lưu vào file
    df.to_csv('tracking_data.csv', index=False)
    
    print(f"✅ Đã tạo {len(df)} mẫu dữ liệu giả lập")
    print(f"\n📊 Thống kê:")
    print(f"   - Tổng mẫu: {len(df)}")
    print(f"   - Thời gian TB: {df['time_on_page'].mean():.2f}s")
    print(f"   - Desktop: {len(df[df['device_type']=='desktop'])}")
    print(f"   - Mobile: {len(df[df['device_type']=='mobile'])}")
    print(f"\n   Phân bố theo trang:")
    print(df['page_type'].value_counts())
    print(f"\n   Phân bố theo sản phẩm:")
    print(df[df['product_id'] > 0]['product_id'].value_counts())
    print(f"\n💡 Model đã sẵn sàng để train!")
    print(f"🎯 20% dữ liệu còn lại sẽ đến từ người dùng thực tế")

if __name__ == '__main__':
    initialize_tracking_data()
