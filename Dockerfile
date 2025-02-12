FROM python:3.8-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tạo thư mục SSL và copy certificates
RUN mkdir -p /app/ssl
COPY ./ssl/cert.pem /app/ssl/
COPY ./ssl/key.pem /app/ssl/
COPY . .

EXPOSE 4000

CMD ["gunicorn", "--bind", "0.0.0.0:443", "--certfile", "/app/ssl/cert.pem", "--keyfile", "/app/ssl/key.pem", "--workers", "4", "--threads", "2", "wsgi:app"]