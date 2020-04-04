from Crypto.Cipher import AES
import struct
from set1.xor import xor
import base64

def ctr_helper(input, key, nonce):
    # pt can be any sized plaintext
    # xor it with 16 byte chunks of key stream
    cipher = AES.new(key, mode=AES.MODE_ECB)
    output = b""
    for i in range(0, len(input), 16):
        # Create a key
        # q = long = 8 bytes
        # < mean LE
        a = struct.pack("<qq", nonce, i // 16)
        e = cipher.encrypt(a)
        output += xor(input[i:i+16], e)
    return output

def encrypt_ctr(pt, key, nonce):
    return ctr_helper(pt, key, nonce)

def decrypt_ctr(ct, key, nonce):
    return ctr_helper(ct, key, nonce)

if __name__ == '__main__':
    test = bytes("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==", 'utf-8')
    t = base64.decodebytes(test)
    key = b"YELLOW SUBMARINE"
    print(decrypt_ctr(encrypt_ctr(b"hello", key, 10), key, 10))
    print(decrypt_ctr(t, key, 0))
