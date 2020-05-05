from set3.ctr_mode import encrypt_ctr, decrypt_ctr
from random import randrange

key = bytes([randrange(255) for _ in range(16)])

def encrypt(input):
    if b';' in input or b'=' in input:
        raise Exception("invalid characters")
    prefix = b"comment1=cooking%20MCs;userdata="
    postfix = b";comment2=%20like%20a%20pound%20of%20bacon"
    return encrypt_ctr(prefix + input + postfix, key, 0)

def is_admin(ct):
    pt = decrypt_ctr(ct, key, 0)
    print(pt)
    return b"admin=true" in pt

if __name__ == "__main__":
    # Goal is same as before - craft an input
    # yields is_admin true
    # 1 + 5 + 1 + 4 = 11 bytes, i.e.
    # prefix is exactly 2 blocks
    ct = encrypt(b"A:admin<true")
    modified_ct = bytearray(ct)
    modified_ct[16*2+1] ^= 1 # flip the bit to add 1 and turn ':' into ;
    modified_ct[16*2+7] ^= 1 # flip the bit to add 1 ant turn '<' into =
    print(is_admin(bytes(modified_ct)))
