# ShopAI - E-commerce với AI Analytics

Trang web bán hàng tích hợp AI để phân tích hành vi khách hàng.

## Tính năng

- 🛍️ Trang web bán hàng đầy đủ (Trang chủ, Sản phẩm, Chi tiết, Liên hệ)
- 🤖 AI tracking tự động theo dõi thời gian xem trang
- 📊 Analytics Dashboard chi tiết
- 📱 Responsive design (Mobile + Desktop)
- 🎨 Bootstrap 5 + Font Awesome

## Cài đặt Local

```bash
# Clone repository
git clone <your-repo-url>
cd <your-repo-name>

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python app_shop.py
```

Truy cập: http://localhost:5001

## Deploy lên Render (Miễn phí)

1. Push code lên GitHub
2. Vào https://render.com → Sign up
3. New → Web Service
4. Connect GitHub repository
5. Cấu hình:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app_shop:app`
6. Deploy!

## Deploy lên Railway (Miễn phí)

1. Push code lên GitHub
2. Vào https://railway.app → Sign up
3. New Project → Deploy from GitHub
4. Chọn repository
5. Tự động deploy!

## Deploy lên PythonAnywhere (Miễn phí)

1. Đăng ký tại https://www.pythonanywhere.com
2. Upload code hoặc clone từ GitHub
3. Cấu hình Web App với Flask
4. Done!

## Công nghệ

- Backend: Flask (Python)
- Frontend: Bootstrap 5, HTML/CSS/JS
- AI/ML: Scikit-learn, Pandas
- Database: CSV (có thể nâng cấp lên SQLite/PostgreSQL)

## License

MIT
