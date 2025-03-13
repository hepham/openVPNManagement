FROM python:3.8-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tạo thư mục SSL và copy certificates (có thể bỏ nếu không cần)
RUN mkdir -p /app/ssl
# COPY ./ssl/cert.pem /app/ssl/ 
# COPY ./ssl/key.pem /app/ssl/   
COPY . .

EXPOSE 4000

CMD ["gunicorn", "--bind", "0.0.0.0:4000", "wsgi:app"]  