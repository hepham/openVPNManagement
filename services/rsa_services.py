from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import base64
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()

def encrypt(public_key,message):
    public_key_pem=f"""
-----BEGIN PUBLIC KEY-----
{public_key}
-----END PUBLIC KEY-----"""
    public_key = serialization.load_pem_public_key(
    public_key_pem.encode('utf-8'),
    backend=default_backend()
)
    encrypted = public_key.encrypt(
        message.encode("utf-8"),
        padding.PKCS1v15() 
    )
    encrypted_base64 = base64.b64encode(encrypted).decode("utf-8")
    print(encrypted_base64)
    return encrypted_base64

def decrypt(private_key_pem,encrypt_message):
    private_key = serialization.load_pem_private_key(
    private_key_pem.encode('utf-8'),
    password=None,
    backend=default_backend()
)

    encrypted_data = base64.b64decode(encrypt_message)
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.PKCS1v15()  
    )

    return decrypted_data.decode('utf-8')