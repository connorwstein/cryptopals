from Crypto.Cipher import AES
import base64
key = "YELLOW SUBMARINE"

def decrypt_aes_ecb(key, msg):
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return cipher.decrypt(msg)

with open('7.txt', 'rb') as f:
    contents = base64.decodebytes(f.read())
print(contents)
print(decrypt_aes_ecb(bytes(key, 'utf-8'), contents))