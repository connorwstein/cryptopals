from set2.cbc_mode import encrypt_aes_cbc, decrypt_aes_cbc
from random import randrange
from set1.xor import xor

# key = bytes([randrange(255) for _ in range(16)])
key = bytes([132, 46, 187, 138, 67, 87, 199, 53, 99, 118, 246, 89, 64, 99, 32, 173])
errmsg = b"non-ascii byte found in "

def encrypt(input):
    if b';' in input or b'=' in input:
        raise Exception("invalid characters")
    for b in input:
        if b > 128:
            raise Exception("non-ascii byte", b)
    # prefix = b"comment1=cooking%20MCs;userdata=" #
    # postfix = b";comment2=%20like%20a%20pound%20of%20bacon"
    return encrypt_aes_cbc(key, input, 16, key)

def decrypt(ct):
    pt = decrypt_aes_cbc(key, ct, 16, key)
    non_ascii_byte = False
    for i, b in enumerate(pt):
        if b > 128:
            non_ascii_byte = True
    if non_ascii_byte:
        return errmsg + pt
    return pt

if __name__ == "__main__":
    pt = b"yellow submarineyellow submarineyellow submarine"
    ct = encrypt(pt) # 3 blocks encrypted
    ct_modified = ct[:16] + bytes([0]*16) + ct[:16]
    pt_t = decrypt(ct_modified)
    pt_t = pt_t[len(errmsg):]
    recovered_key = xor(b"yellow submarine", pt_t[16*2:16*3])
    assert(key == recovered_key)
