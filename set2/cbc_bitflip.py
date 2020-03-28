from set2.byte_ecb_decryption import random_aes_key
from set2.cbc_mode import encrypt_aes_cbc, decrypt_aes_cbc
from set2.pkcs_padding import pad_pkcs7
from random import randrange

key = random_aes_key()
iv = b'\x00' * 16

def encrypt(input):
    if b';' in input or b'=' in input:
        raise Exception("invalid characters")
    prefix = b"comment1=cooking%20MCs;userdata="
    postfix = b";comment2=%20like%20a%20pound%20of%20bacon"
    return encrypt_aes_cbc(key, prefix + input + postfix, 16, iv)

def is_admin(ct):
    pt = decrypt_aes_cbc(key, ct, 16, iv)
    print(pt)
    return b"admin=true" in pt

if __name__ == '__main__':
    ct = encrypt(bytes("AAAAAAAAAAAAAAAAaaaaaa:admin<true", 'utf-8'))
    # Goal is to get this thing to return true by manipulating the payload.
    # prefix is 32 bytes -> convenient 2 blocks exactly
    # We add a sacrificial block of junk (A's), tune the bytes
    # so that the next cipher block decrypts to something different.
    # Specifically to make it decrypt to aaaaa;admin=true as a whole block.
    # : is 1 less than ;
    # < is 1 less than =
    # Both happen to be even (end in 0) so if we just flip the last bit,
    # we'll make it decrypt to what we want.

    # Note that it destroys your plaintext block you are in so we need one block of junk first
    # Also I guess this wouldn't work if they were looking for specific bytes as the payload
    # like utf-8 encoded bytes.
    index_byte_1 = 16*2+6
    index_byte_2 = 16*2+12
    modified_ct = bytearray(ct)
    modified_ct[16*2+6] ^= 1 # flip the last bit to add 1
    modified_ct[16*2+12] ^= 1 # flip the last bit to add 1
    print(is_admin(bytes(modified_ct)))





