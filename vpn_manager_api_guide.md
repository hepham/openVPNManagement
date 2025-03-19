# Hướng dẫn sử dụng API OpenVPN Management

## Giới thiệu

Tài liệu này mô tả các API của hệ thống OpenVPN Management và luồng giao tiếp giữa ứng dụng client và server VPN Manager. Hệ thống sử dụng các cơ chế bảo mật như mã hóa RSA và AES để đảm bảo tính bảo mật trong quá trình truyền thông.

## Mô hình hoạt động

Hệ thống OpenVPN Management hoạt động theo mô hình Client-Server, trong đó:

1. **Máy khách (Client)**: Ứng dụng người dùng gọi các API để:
   - Lấy danh sách máy chủ VPN
   - Lấy khóa RSA để mã hóa thông tin
   - Nhận cấu hình VPN (WireGuard) để kết nối

2. **Máy chủ (Server)**: Quản lý danh sách server VPN, xử lý yêu cầu từ client và tương tác với các máy chủ VPN thực tế.

## Luồng xử lý chính

### 1. Khởi tạo kết nối an toàn

```mermaid
sequenceDiagram
    Client->>VPNManager: GET /key/{username}
    VPNManager->>VPNManager: Tạo cặp khóa RSA
    VPNManager->>Client: Public Key
```

### 2. Lấy danh sách server VPN

```mermaid
sequenceDiagram
    Client->>VPNManager: GET /listServer
    VPNManager->>Database: Truy vấn danh sách server
    Database->>VPNManager: Dữ liệu server
    VPNManager->>VPNManager: Mã hóa AES
    VPNManager->>Client: Danh sách server đã mã hóa
```

### 3. Lấy cấu hình VPN

```mermaid
sequenceDiagram
    Client->>Client: Mã hóa thông tin "user:{username} server_id:{id}"
    Client->>VPNManager: POST /config
    VPNManager->>VPNManager: Giải mã thông tin người dùng
    VPNManager->>VPNServer: Yêu cầu cấu hình WireGuard
    VPNServer->>VPNManager: Cấu hình WireGuard
    VPNManager->>VPNManager: Mã hóa thông tin nhạy cảm
    VPNManager->>Client: Cấu hình VPN đã mã hóa
```

## API Reference

### RSA Controller

#### 1. Lấy Public Key
```
GET /key/{username}
```

**Mô tả:** Tạo cặp khóa RSA mới cho người dùng và lưu trữ trong Redis. Trả về public key cho client.

**Tham số:**
- `username`: Tên người dùng cần tạo khóa

**Phản hồi thành công:**
```json
{
  "key": "[public_key_string]"
}
```

**Mã trạng thái:** 201 Created

#### 2. Lấy thông tin tất cả người dùng (chỉ cho mục đích gỡ lỗi)
```
GET /key/all
```

**Mô tả:** Trả về thông tin về tất cả các khóa người dùng được lưu trữ.

**Phản hồi thành công:**
```json
{
  "message": "Ok"
}
```

### Server Controller

#### 1. Danh sách Server
```
GET /listServer
```

**Mô tả:** Trả về danh sách tất cả các máy chủ VPN có sẵn đã được mã hóa AES.

**Phản hồi thành công:**
```json
{
  "message": "[encrypted_server_list]"
}
```

**Giải mã dữ liệu:** Client cần sử dụng khóa AES được cung cấp trước để giải mã dữ liệu. Sau khi giải mã, chuỗi JSON sẽ chứa mảng các đối tượng server với thông tin sau:
```json
[
  {
    "id": 1,
    "IP": "http://3.139.103.95:10086",
    "country": "United State",
    "city": "Ohio",
    "flag": "vn.png",
    "isFree": true,
    "category": "Videos",
    "description": "Telemundo",
    "latitude": "10.762622",
    "longitude": "106.660172",
    "region": "Ohio",
    "postal": "70000"
  }
]
```

#### 2. Thêm Server
```
POST /server
```

**Mô tả:** Thêm một máy chủ VPN mới vào hệ thống.

**Body:**
```json
{
  "IP": "https://example.com",
  "city": "Ho Chi Minh",
  "flag": "vn.png",
  "isFree": true,
  "description": "Server VPN tại Việt Nam",
  "category": "Free"
}
```

**Phản hồi thành công:**
```json
{
  "message": "Server added successfully"
}
```

**Mã trạng thái:** 201 Created

#### 3. Thêm nhiều Server
```
POST /server/list
```

**Mô tả:** Thêm nhiều máy chủ VPN cùng lúc.

**Body:**
```json
[
  {
    "IP": "https://example1.com",
    "flag": "vn.png",
    "isFree": true,
    "description": "Server VPN tại Việt Nam 1",
    "category": "Free"
  },
  {
    "IP": "https://example2.com",
    "flag": "sg.png",
    "isFree": false,
    "description": "Server VPN tại Singapore",
    "category": "Premium"
  }
]
```

#### 4. Lấy cấu hình VPN
```
POST /config
```

**Mô tả:** Lấy cấu hình WireGuard cho kết nối VPN. Thông tin người dùng và server được mã hóa RSA.

**Body:**
```json
{
  "message": "[encrypted_message]",
  "public_key": "[client_public_key]",
  "user": "username"
}
```

**Lưu ý:** `encrypted_message` là chuỗi được mã hóa của chuỗi gốc "user:{username} server_id:{id}"

**Phản hồi thành công:**
```json
{
  "certificate": "[encrypted_certificate]",
  "config": "[wireguard_config_template]"
}
```

**Mã trạng thái:** 200 OK

## Quy trình sử dụng

### Bước 1: Khởi tạo kết nối an toàn
1. Gọi API `GET /key/{username}` để nhận public key từ server
2. Lưu public key để sử dụng cho việc mã hóa thông điệp sau này

### Bước 2: Lấy danh sách server VPN
1. Gọi API `GET /listServer` để nhận danh sách server đã mã hóa
2. Sử dụng khóa AES (mặc định là "SMJUH41TkNyChU8c5kWPiA==") để giải mã danh sách server
3. Hiển thị danh sách server để người dùng lựa chọn

### Bước 3: Lấy cấu hình VPN
1. Khi người dùng chọn một server VPN, tạo chuỗi thông tin: "user:{username} server_id:{id}"
2. Sử dụng public key từ bước 1 để mã hóa chuỗi này
3. Gọi API `POST /config` với thông tin đã mã hóa, public key và tên người dùng
4. Nhận cấu hình WireGuard đã mã hóa từ server
5. Giải mã thông tin nhạy cảm sử dụng khóa RSA
6. Sử dụng cấu hình WireGuard để thiết lập kết nối VPN

## Cơ chế bảo mật

Hệ thống sử dụng kết hợp hai cơ chế mã hóa:

1. **Mã hóa RSA**: Sử dụng cho việc truyền thông tin nhạy cảm từ client đến server
   - Độ dài khóa: 2048 bit
   - Client sử dụng public key của server để mã hóa
   - Server sử dụng private key để giải mã

2. **Mã hóa AES**: Sử dụng cho việc mã hóa danh sách server
   - Chế độ mã hóa: ECB
   - Cùng một khóa AES được sử dụng trên client và server

## Các lỗi thường gặp

| Mã lỗi | Mô tả | Giải pháp |
|--------|-------|-----------|
| 400    | Bad Request - Định dạng yêu cầu không hợp lệ | Kiểm tra định dạng thông điệp |
| 500    | Error decrypt - Không thể giải mã thông điệp | Kiểm tra khóa và thông điệp |
| 503    | Server down - Máy chủ VPN không khả dụng | Thử lại sau hoặc chọn server khác |

## Ví dụ mã nguồn

### Client - Lấy danh sách server
```python
import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

def decrypt_with_aes(encrypted_data, key):
    key_bytes = key.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted_bytes = b64decode(encrypted_data)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted = unpad(decrypted_padded, AES.block_size)
    return decrypted.decode('utf-8')

# Lấy danh sách server
response = requests.get("http://localhost:4000/listServer")
encrypted_message = response.json()["message"]

# Giải mã
key = "SMJUH41TkNyChU8c5kWPiA=="
server_list_json = decrypt_with_aes(encrypted_message, key)
server_list = json.loads(server_list_json)

# Hiển thị danh sách server
for server in server_list:
    print(f"{server['country']} - {server['city']} - {server['isFree']}")
```

### Client - Lấy cấu hình VPN
```python
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

# Lấy public key
username = "user123"
response = requests.get(f"http://localhost:4000/key/{username}")
public_key = response.json()["key"]

# Chuẩn bị thông tin để mã hóa
message = f"user:{username} server_id:1"

# Mã hóa thông điệp
public_key_pem = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
public_key_obj = serialization.load_pem_public_key(
    public_key_pem.encode('utf-8'),
    backend=default_backend()
)
encrypted = public_key_obj.encrypt(
    message.encode("utf-8"),
    padding.PKCS1v15()
)
encrypted_base64 = base64.b64encode(encrypted).decode("utf-8")

# Gửi yêu cầu lấy cấu hình
config_response = requests.post(
    "http://localhost:4000/config",
    json={
        "message": encrypted_base64,
        "public_key": public_key,
        "user": username
    }
)

# Nhận cấu hình đã mã hóa
if config_response.status_code == 200:
    data = config_response.json()
    certificate = data["certificate"]
    config_template = data["config"]
    print("Đã nhận cấu hình VPN thành công")
    # Tiếp tục xử lý, giải mã certificate và tạo file cấu hình
else:
    print(f"Lỗi: {config_response.json()['message']}")
```

## Kết luận

OpenVPN Management API cung cấp các endpoint để ứng dụng client có thể kết nối an toàn tới các máy chủ VPN. Hệ thống sử dụng các cơ chế mã hóa mạnh để bảo vệ thông tin nhạy cảm trong quá trình truyền thông. Ứng dụng client cần tuân thủ đúng các bước và quy trình mã hóa/giải mã để sử dụng API một cách hiệu quả. 