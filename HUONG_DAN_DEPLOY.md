# Hướng Dẫn Deploy Dự Án

## Bước 1: Push code lên GitHub

```bash
# Khởi tạo Git (nếu chưa có)
git init

# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit - ShopAI project"

# Tạo repository trên GitHub (vào github.com → New repository)
# Sau đó link với local:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Bước 2: Deploy lên Render (KHUYẾN NGHỊ - Miễn phí & Dễ nhất)

### Tại sao chọn Render?
- ✅ Miễn phí vĩnh viễn
- ✅ Tự động deploy khi push code
- ✅ Hỗ trợ Python/Flask tốt
- ✅ Có SSL miễn phí (HTTPS)
- ✅ Không cần credit card

### Các bước:

1. **Đăng ký Render**
   - Vào https://render.com
   - Sign up bằng GitHub account

2. **Tạo Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository của bạn
   - Chọn repository vừa push

3. **Cấu hình**
   ```
   Name: shopai (hoặc tên bạn muốn)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app_shop:app
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Đợi 2-3 phút
   - Nhận link: https://shopai-xxxx.onrender.com

5. **Lưu ý**
   - Free tier sẽ sleep sau 15 phút không dùng
   - Lần đầu truy cập sau khi sleep sẽ mất ~30s để wake up

## Bước 3: Deploy lên Railway (Thay thế)

1. Vào https://railway.app
2. Sign up với GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Chọn repository
5. Railway tự động detect Flask và deploy
6. Nhận link: https://shopai.railway.app

## Bước 4: Deploy lên PythonAnywhere (Thay thế)

1. Đăng ký https://www.pythonanywhere.com (Free account)
2. Vào "Web" tab → "Add a new web app"
3. Chọn "Manual configuration" → Python 3.10
4. Upload code hoặc clone từ GitHub:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```
5. Cấu hình WSGI file:
   ```python
   import sys
   path = '/home/YOUR_USERNAME/YOUR_REPO_NAME'
   if path not in sys.path:
       sys.path.append(path)
   
   from app_shop import app as application
   ```
6. Install requirements trong Console:
   ```bash
   pip install -r requirements.txt
   ```
7. Reload web app
8. Truy cập: https://YOUR_USERNAME.pythonanywhere.com

## So sánh các nền tảng

| Nền tảng | Miễn phí | Dễ dùng | Tốc độ | SSL | Giới hạn |
|----------|----------|---------|--------|-----|----------|
| **Render** | ✅ | ⭐⭐⭐⭐⭐ | Nhanh | ✅ | Sleep sau 15p |
| **Railway** | ✅ | ⭐⭐⭐⭐⭐ | Rất nhanh | ✅ | 500h/tháng |
| **PythonAnywhere** | ✅ | ⭐⭐⭐ | Trung bình | ✅ | 1 web app |
| **Heroku** | ❌ (trả phí) | ⭐⭐⭐⭐ | Nhanh | ✅ | - |

## Khuyến nghị

**Dùng Render** - Dễ nhất, miễn phí, tự động deploy!

## Lưu ý quan trọng

1. **File CSV**: Trên hosting miễn phí, file CSV sẽ bị reset khi restart. Để lưu dữ liệu lâu dài, nên dùng:
   - SQLite (miễn phí)
   - PostgreSQL (Render cung cấp miễn phí)
   - MongoDB Atlas (miễn phí)

2. **Environment Variables**: Nếu có thông tin nhạy cảm, dùng biến môi trường thay vì hard-code.

3. **Debug Mode**: Nhớ tắt debug mode khi deploy:
   ```python
   if __name__ == '__main__':
       app.run(debug=False)  # Đổi thành False
   ```

## Cần hỗ trợ?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- PythonAnywhere Help: https://help.pythonanywhere.com
