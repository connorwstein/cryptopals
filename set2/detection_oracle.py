from set2.cbc_mode import encrypt_aes_cbc
from set2.pkcs_padding import pad_pkcs7
from set1.aes_ecb import encrypt_aes_ecb
from set1.aes_ecb_detect import is_ecb
from random import randrange

from enum import Enum
class Mode(Enum):
    CBC = 1
    ECB = 2

def random_aes_key():
    return bytes([randrange(255) for _ in range(16)])

def encryption_oracle(msg):
    # Append 5-10 bytes randomly before and 5-10 bytes after
    # 0.5 ecb 0.5 cbc
    ecb = randrange(2) == 1
    msg = bytes(random_aes_key()[0:randrange(10)] + msg + bytes(random_aes_key()[0:randrange(10)]))
    if ecb:
        return encrypt_aes_ecb(random_aes_key(), pad_pkcs7(msg, 16)), Mode.ECB
    else:
        return encrypt_aes_cbc(random_aes_key(), msg, 16, random_aes_key()), Mode.CBC

def detection_oracle(ct):
    """Determine if the ct is ecb or cbc"""
    return Mode.ECB if is_ecb(ct, 16) else Mode.CBC

if __name__ == '__main__':
    for i in range(100):
        ct, mode = encryption_oracle(b'YELLOW SUBMARINE'*20)
        detected_mode = detection_oracle(ct)
