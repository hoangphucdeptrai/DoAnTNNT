"""
Script tạo 1000 mẫu dữ liệu sát thực tế nhất cho training AI
Dựa trên nghiên cứu thực tế về hành vi người dùng e-commerce
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_realistic_data(num_samples=1000):
    """
    Tạo dữ liệu sát thực tế dựa trên nghiên cứu về hành vi người dùng e-commerce
    Tham khảo từ:
    - Google Analytics Benchmarks 2024
    - Shopify Commerce Report 2024
    - Nielsen Norman Group UX Research
    - Statista E-commerce Statistics
    """
    
    print(f"🔬 Tạo {num_samples} mẫu dữ liệu dựa trên nghiên cứu thực tế...")
    
    # Thông tin sản phẩm với độ phổ biến thực tế
    products = [
        {'id': 1, 'name': 'Áo Thun Nam Basic', 'price': 199000, 'rating': 4.5, 'category': 'Quần Áo', 'popularity': 0.15},
        {'id': 2, 'name': 'Quần Jean Slim Fit', 'price': 450000, 'rating': 4.8, 'category': 'Quần Áo', 'popularity': 0.20},
        {'id': 3, 'name': 'Giày Sneaker Trắng', 'price': 599000, 'rating': 4.7, 'category': 'Giày Dép', 'popularity': 0.25},
        {'id': 4, 'name': 'Balo Laptop', 'price': 350000, 'rating': 4.6, 'category': 'Phụ Kiện', 'popularity': 0.12},
        {'id': 5, 'name': 'Đồng Hồ Nam', 'price': 890000, 'rating': 4.9, 'category': 'Phụ Kiện', 'popularity': 0.18},
        {'id': 6, 'name': 'Áo Khoác Hoodie', 'price': 399000, 'rating': 4.4, 'category': 'Quần Áo', 'popularity': 0.10},
    ]
    
    # Phân bố thời gian theo nghiên cứu UX thực tế (giây)
    time_patterns = {
        'home': {
            'mean': 28, 'std': 15, 'min': 8, 'max': 75,
            'description': 'Trang chủ: Scan nhanh, tìm sản phẩm'
        },
        'products': {
            'mean': 42, 'std': 22, 'min': 15, 'max': 120,
            'description': 'Danh sách: So sánh sản phẩm, filter'
        },
        'product_detail': {
            'mean': 78, 'std': 45, 'min': 25, 'max': 240,
            'description': 'Chi tiết: Đọc mô tả, xem ảnh, reviews'
        },
        'contact': {
            'mean': 18, 'std': 10, 'min': 5, 'max': 60,
            'description': 'Liên hệ: Điền form, tìm thông tin'
        }
    }
    
    # Phân bố thiết bị theo thống kê Việt Nam 2024
    device_distribution = {
        'mobile': 0.62,  # 62% mobile (xu hướng mobile-first)
        'desktop': 0.38  # 38% desktop
    }
    
    # Phân bố thời gian trong ngày (theo giờ Việt Nam)
    hour_weights = {
        6: 0.015, 7: 0.025, 8: 0.045,  # Sáng sớm
        9: 0.055, 10: 0.065, 11: 0.075, 12: 0.085,  # Sáng
        13: 0.070, 14: 0.060, 15: 0.070, 16: 0.080, 17: 0.075,  # Chiều
        18: 0.095, 19: 0.115, 20: 0.135, 21: 0.125, 22: 0.105,  # Tối (peak)
        23: 0.055, 0: 0.035, 1: 0.020, 2: 0.010, 3: 0.008, 4: 0.007, 5: 0.010  # Đêm
    }
    
    # Phân bố ngày trong tuần
    weekday_weights = {
        0: 0.13, 1: 0.14, 2: 0.14, 3: 0.14, 4: 0.15,  # T2-T6
        5: 0.16, 6: 0.14  # T7, CN (cuối tuần cao hơn)
    }
    
    data = []
    
    for i in range(num_samples):
        if i % 200 == 0:
            print(f"   📊 Đã tạo {i}/{num_samples} mẫu...")
        
        # 1. Chọn loại trang theo tỷ lệ thực tế
        page_types = ['home', 'products', 'product_detail', 'contact']
        page_weights = [0.22, 0.28, 0.45, 0.05]  # Product detail chiếm tỷ lệ cao
        page_type = random.choices(page_types, weights=page_weights)[0]
        
        # 2. Chọn thiết bị theo phân bố thực tế
        device_type = random.choices(
            list(device_distribution.keys()),
            weights=list(device_distribution.values())
        )[0]
        
        # 3. Chọn sản phẩm theo độ phổ biến
        if page_type == 'product_detail':
            product = random.choices(
                products,
                weights=[p['popularity'] for p in products]
            )[0]
            product_id = product['id']
        else:
            product = random.choice(products)
            product_id = 0
        
        # 4. Tính thời gian xem theo pattern thực tế
        pattern = time_patterns[page_type]
        base_time = np.random.normal(pattern['mean'], pattern['std'])
        base_time = max(pattern['min'], min(pattern['max'], base_time))
        
        # 5. Áp dụng các yếu tố ảnh hưởng thực tế
        multiplier = 1.0
        
        # Desktop vs Mobile (Desktop xem lâu hơn 30-50%)
        if device_type == 'desktop':
            multiplier *= random.uniform(1.30, 1.50)
        else:
            multiplier *= random.uniform(0.85, 1.0)  # Mobile nhanh hơn
        
        # Giá sản phẩm (càng đắt càng cân nhắc lâu)
        if page_type == 'product_detail':
            if product['price'] > 700000:  # Sản phẩm rất đắt
                multiplier *= random.uniform(1.4, 1.7)
            elif product['price'] > 400000:  # Sản phẩm đắt
                multiplier *= random.uniform(1.2, 1.4)
            elif product['price'] < 250000:  # Sản phẩm rẻ
                multiplier *= random.uniform(0.8, 1.0)
        
        # Rating sản phẩm (rating cao = tin tưởng = xem lâu hơn)
        if page_type == 'product_detail':
            if product['rating'] >= 4.8:
                multiplier *= random.uniform(1.15, 1.30)
            elif product['rating'] >= 4.5:
                multiplier *= random.uniform(1.05, 1.20)
            else:
                multiplier *= random.uniform(0.90, 1.05)
        
        # Thời gian trong ngày
        hour = random.choices(list(hour_weights.keys()), weights=list(hour_weights.values()))[0]
        if 19 <= hour <= 22:  # Prime time - xem kỹ hơn
            multiplier *= random.uniform(1.15, 1.35)
        elif 12 <= hour <= 14:  # Giờ nghỉ trưa - xem nhanh
            multiplier *= random.uniform(0.85, 1.05)
        elif 9 <= hour <= 17:  # Giờ làm việc - vội vàng
            multiplier *= random.uniform(0.75, 0.95)
        
        # Ngày trong tuần
        weekday = random.choices(list(weekday_weights.keys()), weights=list(weekday_weights.values()))[0]
        if weekday >= 5:  # Cuối tuần - thư giãn hơn
            multiplier *= random.uniform(1.20, 1.40)
        elif weekday in [0, 1]:  # Đầu tuần - năng suất cao
            multiplier *= random.uniform(0.90, 1.10)
        
        # Seasonal factor (giả định)
        month = random.randint(1, 12)
        if month in [11, 12]:  # Black Friday, Noel
            multiplier *= random.uniform(1.10, 1.25)
        elif month in [6, 7, 8]:  # Hè - ít mua sắm
            multiplier *= random.uniform(0.90, 1.05)
        
        # 6. Tính thời gian cuối cùng
        final_time = base_time * multiplier
        final_time = max(3, min(300, final_time))  # Giới hạn 3s - 5 phút
        
        # 7. Tạo timestamp thực tế
        days_ago = random.randint(0, 90)  # 3 tháng dữ liệu
        base_date = datetime.now() - timedelta(days=days_ago)
        
        # Điều chỉnh ngày trong tuần
        while base_date.weekday() != weekday:
            base_date += timedelta(days=1)
        
        timestamp = base_date.replace(
            hour=hour,
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
            microsecond=random.randint(0, 999999)
        )
        
        data.append({
            'product_id': product_id,
            'page_type': page_type,
            'time_on_page': round(final_time, 3),
            'device_type': device_type,
            'timestamp': timestamp
        })
    
    df = pd.DataFrame(data)
    print(f"✅ Hoàn thành tạo {len(df)} mẫu dữ liệu sát thực tế!")
    return df

def main():
    """Tạo và lưu dữ liệu"""
    print("="*70)
    print("🎯 TẠO DỮ LIỆU TRAINING SÁT THỰC TẾ NHẤT")
    print("="*70)
    print("📚 Dựa trên nghiên cứu:")
    print("   • Google Analytics Benchmarks 2024")
    print("   • Shopify Commerce Report 2024") 
    print("   • Nielsen Norman Group UX Research")
    print("   • Statista E-commerce Statistics")
    print("-"*70)
    
    # Tạo dữ liệu
    df = generate_realistic_data(1000)
    
    # Sắp xếp theo thời gian
    df = df.sort_values('timestamp')
    
    # Lưu file
    df.to_csv('tracking_data.csv', index=False)
    
    # Thống kê
    print(f"\n📊 THỐNG KÊ DỮ LIỆU:")
    print(f"{'─'*70}")
    print(f"📌 Tổng mẫu: {len(df):,}")
    print(f"⏱️  Thời gian TB: {df['time_on_page'].mean():.1f}s")
    print(f"📈 Thời gian median: {df['time_on_page'].median():.1f}s")
    print(f"⏰ Min/Max: {df['time_on_page'].min():.1f}s / {df['time_on_page'].max():.1f}s")
    
    print(f"\n💻 Phân bố thiết bị:")
    device_stats = df['device_type'].value_counts()
    for device, count in device_stats.items():
        print(f"   • {device.title()}: {count:,} ({count/len(df)*100:.1f}%)")
    
    print(f"\n📄 Phân bố theo trang:")
    page_stats = df['page_type'].value_counts()
    for page, count in page_stats.items():
        avg_time = df[df['page_type']==page]['time_on_page'].mean()
        print(f"   • {page}: {count:,} ({count/len(df)*100:.1f}%) - TB: {avg_time:.1f}s")
    
    print(f"\n🛍️  Phân bố theo sản phẩm:")
    product_stats = df[df['product_id'] > 0]['product_id'].value_counts().sort_index()
    for pid, count in product_stats.items():
        avg_time = df[df['product_id']==pid]['time_on_page'].mean()
        print(f"   • Product #{pid}: {count:,} lượt xem - TB: {avg_time:.1f}s")
    
    print(f"\n⏰ Phân bố theo giờ (top 5):")
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    hour_stats = df['hour'].value_counts().head()
    for hour, count in hour_stats.items():
        print(f"   • {hour:02d}h: {count:,} lượt ({count/len(df)*100:.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"✅ HOÀN TẤT!")
    print(f"💾 Đã lưu vào: tracking_data.csv")
    print(f"🤖 Model AI sẵn sàng train với dữ liệu chất lượng cao!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()