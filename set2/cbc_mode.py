from set1.aes_ecb_decrypt import encrypt_aes_ecb, decrypt_aes_ecb
from set1.xor import xor
from set2.pkcs_padding import pad_pkcs7
import base64

def cbc_encrypt(key, msg, block_size, iv):
    ct_prev, ct, i = iv, [], 0
    while i < len(msg) / block_size:
        print(msg[i*block_size:(i+1)*block_size])
        ct_block = encrypt_aes_ecb(key, xor(ct_prev, msg[i*block_size:(i+1)*block_size]))
        ct.append(ct_block)
        ct_prev = ct_block
        i += 1
    return b''.join(ct)

def cbc_decrypt(key, msg, block_size, iv):
    ct_prev, pt, i = iv, [], 0
    while i < len(msg) / block_size:
        ct = msg[i*block_size:(i+1)*block_size]
        pt_block = xor(ct_prev, decrypt_aes_ecb(key, ct))
        pt.append(pt_block)
        ct_prev = ct
        i += 1
    return b''.join(pt)

if __name__ == '__main__':
    ct = cbc_encrypt(b'YELLOW SUBMARINE',
                     pad_pkcs7(b'hello world hello world hello world hello world', 16),
                     16, b'\x00' * 16)
    print(cbc_decrypt(b'YELLOW SUBMARINE', ct, 16, b'\x00' * 16))
    with open('10.txt', 'rb') as f:
        msg = base64.decodebytes(f.read())
    print(cbc_decrypt(b'YELLOW SUBMARINE', pad_pkcs7(msg, 16), 16, b'\x00' * 16))


