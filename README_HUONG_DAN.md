# Hướng dẫn chạy dự án với Ngrok

## Bước 1: Cài đặt thư viện Python
```bash
pip install -r requirements.txt
```

## Bước 2: Cài đặt Ngrok

### Cách 1: Tải về từ trang chủ
1. Truy cập: https://ngrok.com/download
2. Tải về và giải nén
3. Đăng ký tài khoản miễn phí tại: https://dashboard.ngrok.com/signup
4. Lấy authtoken tại: https://dashboard.ngrok.com/get-started/your-authtoken
5. Chạy lệnh: `ngrok config add-authtoken <YOUR_TOKEN>`

### Cách 2: Cài qua Chocolatey (Windows)
```bash
choco install ngrok
```

## Bước 3: Chạy Flask Server
Mở terminal thứ nhất và chạy:
```bash
python app.py
```

Server sẽ chạy tại: http://localhost:5000

## Bước 4: Chạy Ngrok
Mở terminal thứ hai và chạy:
```bash
ngrok http 5000
```

Ngrok sẽ tạo ra URL công khai dạng: `https://xxxx-xxxx-xxxx.ngrok-free.app`

## Bước 5: Truy cập
- Sao chép URL từ ngrok
- Chia sẻ URL này cho bất kỳ ai để họ có thể truy cập dự án của bạn!

## Lưu ý:
- Phiên bản miễn phí của ngrok sẽ đổi URL mỗi khi khởi động lại
- Kết nối sẽ bị ngắt sau 2 giờ (cần chạy lại)
- Để có URL cố định, nâng cấp lên gói trả phí

## Các lựa chọn thay thế miễn phí khác:
- **LocalTunnel**: `npm install -g localtunnel` → `lt --port 5000`
- **Serveo**: `ssh -R 80:localhost:5000 serveo.net`
- **Cloudflare Tunnel**: Miễn phí, không giới hạn thời gian
