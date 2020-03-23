from set1.aes_ecb import encrypt_aes_ecb, decrypt_aes_ecb
from set1.xor import xor
from set2.pkcs_padding import pad_pkcs7
import base64

def encrypt_aes_cbc(key, msg, block_size, iv):
    msg = pad_pkcs7(msg, block_size)
    ct_prev, ct, i = iv, [], 0
    while i < len(msg) / block_size:
        ct_block = encrypt_aes_ecb(key, xor(ct_prev, msg[i*block_size:(i+1)*block_size]))
        ct.append(ct_block)
        ct_prev = ct_block
        i += 1
    return b''.join(ct)

def decrypt_aes_cbc(key, msg, block_size, iv):
    ct_prev, pt, i = iv, [], 0
    while i < len(msg) / block_size:
        ct = msg[i*block_size:(i+1)*block_size]
        pt_block = xor(ct_prev, decrypt_aes_ecb(key, ct))
        pt.append(pt_block)
        ct_prev = ct
        i += 1
    return b''.join(pt)

if __name__ == '__main__':
    ct = encrypt_aes_cbc(b'YELLOW SUBMARINE',
                     b'hello world hello world hello world hello world',
                     16, b'\x00' * 16)
    print(decrypt_aes_cbc(b'YELLOW SUBMARINE', ct, 16, b'\x00' * 16))
    with open('10.txt', 'rb') as f:
        msg = base64.decodebytes(f.read())
    print(decrypt_aes_cbc(b'YELLOW SUBMARINE', msg, 16, b'\x00' * 16))


