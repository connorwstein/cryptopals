from Crypto.Cipher import AES
import base64
key = "YELLOW SUBMARINE"

def decrypt_aes_ecb(key, msg):
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return cipher.decrypt(msg)

def encrypt_aes_ecb(key, msg):
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return cipher.encrypt(msg)

def decrypt_aes_ecb_(key, msg, block_size, cipher):
    # Break up the msg into blocks and for each block call the cipher
    blocks, rem = divmod(len(msg), block_size)
    pt = [] # list of bytes objects
    i = 0
    while i < blocks:
        pt.append(cipher.decrypt(msg[i*block_size:(i+1)*block_size]))
        i += 1
    if rem > 0:
        pt.append(cipher.decrypt[msg[blocks*block_size:]])
    return b''.join(pt)

if __name__ == '__main__':
    with open('7.txt', 'rb') as f:
        contents = base64.decodebytes(f.read())
    print(contents)
    cipher = AES.new(bytes(key, 'utf-8'), mode=AES.MODE_ECB)
    print(decrypt_aes_ecb_(bytes(key, 'utf-8'), contents, 16, cipher))
