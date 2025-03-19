# Hướng dẫn Chạy Dự án OpenVPN Management

## Giới thiệu
Dự án OpenVPN Management được thiết kế để quản lý hiệu quả các máy chủ OpenVPN. Nó cung cấp giao diện thân thiện với người dùng và các công cụ để tạo điều kiện quản lý nhiều phiên bản OpenVPN. Hướng dẫn này sẽ giúp bạn cài đặt và chạy dự án bằng Docker, đảm bảo quá trình thiết lập suôn sẻ.
# Hướng dẫn Chạy Dự án OpenVPN Management

## Giới thiệu
Dự án OpenVPN Management được thiết kế để quản lý hiệu quả các máy chủ OpenVPN. Nó cung cấp giao diện thân thiện với người dùng và các công cụ để tạo điều kiện quản lý nhiều phiên bản OpenVPN. Hướng dẫn này sẽ giúp bạn cài đặt và chạy dự án bằng Docker, đảm bảo quá trình thiết lập suôn sẻ.

## Yêu cầu Hệ thống
Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt các phần mềm sau:
- **Docker**: Phiên bản mới nhất
- **Docker Compose**: Phiên bản mới nhất
## Yêu cầu Hệ thống
Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt các phần mềm sau:
- **Docker**: Phiên bản mới nhất
- **Docker Compose**: Phiên bản mới nhất

## Cấu trúc Dự án
Dự án bao gồm các file và thư mục sau:
- `docker-compose.yml`: File cấu hình cho Docker Compose
- `Dockerfile`: File cấu hình để xây dựng hình ảnh Docker cho ứng dụng
## Cấu trúc Dự án
Dự án bao gồm các file và thư mục sau:
- `docker-compose.yml`: File cấu hình cho Docker Compose
- `Dockerfile`: File cấu hình để xây dựng hình ảnh Docker cho ứng dụng

## Hướng dẫn Cài đặt và Chạy
## Hướng dẫn Cài đặt và Chạy

### Bước 1: Tải Mã Nguồn
Clone hoặc tải mã nguồn của dự án về máy local của bạn bằng lệnh sau:
### Bước 1: Tải Mã Nguồn
Clone hoặc tải mã nguồn của dự án về máy local của bạn bằng lệnh sau:

```bash
git clone https://github.com/hepham/openVPNManagement.git
cd openVPNManagement
```

### Bước 2: Xây dựng và Chạy Dự án
Mở terminal và điều hướng đến thư mục chứa file `docker-compose.yml`. Chạy lệnh sau để xây dựng và khởi động các dịch vụ:
### Bước 2: Xây dựng và Chạy Dự án
Mở terminal và điều hướng đến thư mục chứa file `docker-compose.yml`. Chạy lệnh sau để xây dựng và khởi động các dịch vụ:

```bash
docker-compose up --build -d
```

- Lệnh này sẽ xây dựng hình ảnh Docker và khởi động các dịch vụ ở chế độ detached.
- Lệnh này sẽ xây dựng hình ảnh Docker và khởi động các dịch vụ ở chế độ detached.

### Bước 3: Kiểm tra Trạng thái
Sau khi các dịch vụ đã chạy, bạn có thể kiểm tra trạng thái của chúng bằng lệnh sau:
### Bước 3: Kiểm tra Trạng thái
Sau khi các dịch vụ đã chạy, bạn có thể kiểm tra trạng thái của chúng bằng lệnh sau:

```bash
docker-compose ps
```

### Bước 4: Kiểm tra Logs
Nếu bạn cần kiểm tra logs để theo dõi hoạt động của ứng dụng, bạn có thể sử dụng các lệnh sau:

- Để xem logs của dịch vụ web:
- Để xem logs của dịch vụ web:
  ```bash
  docker-compose logs web
  ```

### Bước 5: Dừng Các Dịch vụ
Khi bạn muốn dừng các dịch vụ, bạn có thể sử dụng lệnh sau:
### Bước 5: Dừng Các Dịch vụ
Khi bạn muốn dừng các dịch vụ, bạn có thể sử dụng lệnh sau:

```bash
docker-compose down
```

## Chạy Ứng dụng Trực tiếp

### Bước 1: Tạo và Kích hoạt Môi trường Ảo

```bash
# Tạo môi trường ảo
python3 -m venv venv

# Kích hoạt môi trường ảo
# Trên Linux/Mac:
source venv/bin/activate
# Trên Windows:
.\venv\Scripts\activate
```

### Bước 2: Cài đặt Các Yêu cầu

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy Ứng dụng

#### Lựa chọn 1: Chạy với Python
Nếu bạn muốn chạy ứng dụng trực tiếp bằng Python, bạn có thể thực hiện bằng lệnh sau:

```bash
python wsgi.py
```

- Điều này sẽ khởi động ứng dụng Flask trên cổng mặc định (thường là 4000).
- Điều này sẽ khởi động ứng dụng Flask trên cổng mặc định (thường là 4000).

#### Lựa chọn 2: Chạy với Gunicorn
Để chạy ứng dụng bằng Gunicorn, bạn có thể sử dụng lệnh sau:

```bash
gunicorn --bind 0.0.0.0:4000 wsgi:app
```

- Điều này sẽ khởi động ứng dụng trên cổng 4000.

## Kết luận
Dự án OpenVPN Management cung cấp cách dễ dàng để thiết lập và quản lý các máy chủ OpenVPN. Hãy làm theo các bước trên để đưa dự án vào hoạt động. Nếu bạn gặp bất kỳ vấn đề nào, hãy kiểm tra logs hoặc tham khảo tài liệu chính thức của Docker.
- Điều này sẽ khởi động ứng dụng trên cổng 4000.

## Kết luận
Dự án OpenVPN Management cung cấp cách dễ dàng để thiết lập và quản lý các máy chủ OpenVPN. Hãy làm theo các bước trên để đưa dự án vào hoạt động. Nếu bạn gặp bất kỳ vấn đề nào, hãy kiểm tra logs hoặc tham khảo tài liệu chính thức của Docker.