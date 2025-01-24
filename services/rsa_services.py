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

    # Chuyển đổi khóa sang định dạng PEM
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
        padding.PKCS1v15()  # Phải khớp với Kotlin
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

    encrypted_data = base64.b64decode(encrypt_message)  # Chuyển Base64 → bytes
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.PKCS1v15()  # Padding phải khớp với Kotlin
    )

    return decrypted_data.decode('utf-8')
encrypt("MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs47hFs8mnGI3Hr9XFt2U6FeeGlaUZTamdRCPuBlY88q7tUK+8qdk+2lZ41M3GS1SGCnwS8RgqNM6lJckHplaz31eTAH7CdHszEfrKoq7+MJEzjQ2dO0LCzs30016+HIr/LrDJ0r9XU8Cos+nDq1fwX1qdVKWLz9OkXnlLEfU0xg5WRMse+CD6aiK7GUqF8WDlxaZdWxwQYHGZF9KIbJNZmYA92AF45vMAlCpSIa9yVHUplKtQXRPFky+qKjviHI30ulTdHjYqisrXLV0nkA/qV3EAPH086dyjcQ2/o0/44nTZRBgTvs+cn+1KVqfOyMG5LPyX4Btl625lPeB+QKh5QIDAQAB","Cường Tâm hâm hấp")

private_key_pem = """
-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC4h7+62Uf26Iyu
aYysxe9iT0XGS5EgL7qhN8d4+3JPhrgovi6xW8JlWN4U3tcf6IqeJa/hh2TdNJW2
OFKtkIawAbY6dzetF7l53ay+9NCuMAsKwjs1KGOz98Gk5/BrD6pviDsZS0ZW3pJC
U/JbWIASbHoj7T81m2qPf71AnbxMembF5LP4vGV+eMMp65k47nFnnlanmdeMLRsL
GUwMcKJuz1N8VabYoN1k7pA/8ibS7DsXsLk7o8r3iI86ar3iWTno7ezoiDGLcuoc
0MCU901ZNdZIKl3WZT1V3wFh9up7q0DrGMAmv8wTLLHDxQ9RdAncnwk36wzfMVTH
Xxn79GAZAgMBAAECggEAAgUZ8efT+zoYx7CkbLzZROvyOU4uWDohFF0I5B0xZ05z
8J3KHA7Kd+jCSngVVG1dY/kB+JX5G0ocWMKQ9nSjt3ZI4/wriuggTHd75jaNDgMS
STR5bDiYy7CVbnRLuyaCP++9xIm5kjhrKHF9lA4RAUYt7vu+dv+z6b7FDUtpLBeR
e30p+gbbR7tuJCuiLFEw5PwM7vq0kCputt8wRDUl9IeIgHlumN8CiHbGNmfHFkfV
Zu1/lLt4UOaQS1TjJlbojHxVTPg6C/VWofteyYtYCZr5acAxSH8P2Gz9As88zC3A
MtI6SARiQzE+UyF6pPrKpRnraBihkH1ChuWBvSHFgQKBgQDkseBtXLEozJs7U5eM
kZRjARcPBOa2Jco3wUDGeezQ0TaYZW9ltAm5oJV2A+y27FG7VKPX3Qtz4wt5tcmz
mOt4JBWMN1P1/39vH9Ja3agNZfT39Gvh0q/5a4+2n/Th+igpTrQ5JY6BwtdkMzaY
Um+zraWivuLn2fpGJNgGfLDReQKBgQDOj/hBHAOiOfzmNTY1jOoCXRJcik4bZjqv
mGMrAlu22RNgd32Sp3nzrk/cS+yjhinZCiiNi+WUs91sY45AtGxZfNfmGvr443W8
2ftT2DY9umQhafM07xsQRo4j1ZDalN0kNreEjuHZ1t0J3hpAbsX7doT3IUr0+yrC
h8qhjZf7oQKBgQDDvjQXpwTDpQ0g5FWMrXZSnzY7VriaIxJIUpK8ztMRkGCoY/nL
FSRVy8rhrk5H61Gxg6qRMtOAp07FKAGyRSsWM9x1nU2x+rP6S0RjHeGfRis8p+pG
6WxRkez6JUMWwGTrpj+/whONoVV2oBcUnUqaggCJodTZGcuLijGUq9k0EQKBgQCz
wLdxuXY0CzBYCMBW03ykd+fNnhGgaFLzkbHisJetQ7RIA1PEdnd6phsbAvs3xj3O
gLePjclIoUkz1GLrTdbn/OtIc/wo8I/5utuqOAHjr7sJFNEvJFAx1qRE7Mm0XU0g
AXmsIkbKMd+CgcPohD1Hufi1skQvcg7g4Bhmg/hZYQKBgQC4DWFOezWIn5uXznQW
OLB8fJX2aOgDQLDjZznq3cYl4VriMKnTrJTpuKD0AvTR3AzkmaJk2d9Sojwm2Ava
WqYH8V1CilTlb601u95Uy+zH/hT3cMHYq78Ow+kGu/xVQzD+wwZYS0dQZa22r/NJ
uwmZRe1bdiQYHEPwyI11Zer9PQ==
-----END PRIVATE KEY-----
"""

# Dữ liệu đã mã hóa từ Kotlin (dạng Base64)
encrypted_base64 = "gLqkZ5AC20/OMYBDumyx8BQZNsuu4SRtFNDbgl2N6TraaSH095gJEsfASW7l9BexTzJp6S7b59yzSLR0qbZGHGNECa+DSvoXPEGoolDNJZeKkbW/jhQVg0ksxM+IOda1FcreTHmhaYL9wD1cGrFPXKfMACPOPbqKoE0fqH3t+a8cy4A3awZVdsDSohpq12wiGqfUGCsjaUfl0HQDluiUGuyv96sOdmb49Nl2PFvGRw3V6bUv8YTJrcRWQiPLp2Zl6M/yA2jtlBbl1mv/01HdH/N40sH/1/gOcT4npTeKA+PPFs+WwMrpoz2ic6rYZ7LDOgXIk7UDXBT26hfXQ+ys5g=="

print(decrypt(private_key_pem,encrypted_base64))