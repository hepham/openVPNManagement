from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def generate_key() -> str:
    key = get_random_bytes(16)  # 128-bit = 16 bytes
    return b64encode(key).decode('utf-8')

def encrypt_with_aes(data: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)
    return b64encode(encrypted_bytes).decode('utf-8')

def decrypt_with_aes(encrypted_data: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    
    encrypted_bytes = b64decode(encrypted_data)
    
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted = unpad(decrypted_padded, AES.block_size)
    
    return decrypted.decode('utf-8')
import random
import string
def generate_random_string(length: int = 16) -> str:
    # Ký tự có thể sử dụng: chữ hoa, chữ thường và số
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


