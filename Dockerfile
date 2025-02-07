# Sử dụng Python 3.8 làm base image
FROM python:3.8-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements.txt và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Expose port 5000
EXPOSE 4000

# Chạy ứng dụng với Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:4000", "wsgi:app"]