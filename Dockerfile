# Sử dụng Python 3.8 làm base image
FROM python:3.8-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements.txt và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tạo thư mục SSL và copy certificates
RUN mkdir -p /app/ssl
COPY ./ssl/cert.pem /app/ssl/
COPY ./ssl/key.pem /app/ssl/

# Copy toàn bộ code
COPY . .

# Expose port 443 for HTTPS
EXPOSE 4000

# Chạy ứng dụng với Gunicorn with SSL/HTTPS
CMD ["gunicorn", "--bind", "0.0.0.0:443", "--certfile", "/app/ssl/cert.pem", "--keyfile", "/app/ssl/key.pem", "--workers", "4", "--threads", "2", "wsgi:app"]