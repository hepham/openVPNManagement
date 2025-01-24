import re

def get_user_and_server_id(input_string):
    # Thêm dấu ngoặc đơn để định nghĩa các nhóm
    pattern = r'^user:(\w+)\s+server_id:(\w+)$'
    match = re.match(pattern, input_string)
    if match:
        user = match.group(1)  # Lấy giá trị của user
        server_id = match.group(2)  # Lấy giá trị của server_id
        return {"user": user, "server_id": server_id}
    else:
        return {"error": "Invalid format"}

def check_format(input_string):
    # Biểu thức chính quy để kiểm tra định dạng
    pattern = r'^user:\w+\s+server_id:\w+$'
    
    if re.match(pattern, input_string):
        return True
    return False
def get_certificate(certificate_string):
    # Define the regex pattern
    pattern = r"-----BEGIN CERTIFICATE-----\s*(.*?)\s*-----END CERTIFICATE-----"

    # Use re.search to extract the certificate content
    match = re.search(pattern, certificate_string, re.DOTALL)

    if match:
        certificate_content = match.group(1)  # The certificate content without the BEGIN/END markers
        # print(certificate_content)
        return certificate_content
    else:
        print("Certificate not found.")

# # Ví dụ sử dụng
# if __name__ == "__main__":
#     input_string = "user:hihihaha   server_id:hehe"
#     if check_format(input_string):
#         print("Định dạng chuỗi đúng.")
#     else:
#         print("Định dạng chuỗi không đúng.")