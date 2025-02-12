# openVPNManagement
How to run server:
# create self-signed certificate
mkdir -p ssl
cd ssl
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt
docker-compose up --build -d

# Check logs
docker-compose logs web
docker-compose logs nginx