#AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
import base64
from random import randrange
from set2.byte_ecb_decryption import random_aes_key, decrypt_ecb_with_oracle
from set2.pkcs_padding import pad_pkcs7
from set1.aes_ecb import encrypt_aes_ecb

key = random_aes_key()
random_prefix = bytes([randrange(255)]*randrange(200)) # random bytes

def encryption_oracle(msg):
    secret = base64.decodebytes(bytes(b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' +
                b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
                b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'))
    msg = random_prefix + msg + secret
    return encrypt_aes_ecb(key, pad_pkcs7(msg, 16))

def possible_prefix_lengths():
    # If we compare a no byte arg to a single byte arg,
    # we should be able to tell the length of the random prefix
    # with one-block accuracy, as there will only be one block that changes.
    m0 = encryption_oracle(bytes([]))
    m1 = encryption_oracle(bytes([0]))
    m0_blocks = [m0[i*16:(i+1)*16] for i in range(len(m0)//16 - 1)]
    m1_blocks = [m1[i*16:(i+1)*16] for i in range(len(m1)//16 - 1)]
    block_with_diff = -1
    i = 0
    while i < len(m1_blocks):
        if m1_blocks[i] != m0_blocks[i]:
            block_with_diff = i
            break
        i += 1
    return [block_with_diff*16, (block_with_diff+1)*16]

if __name__ == '__main__':
    # Brute force through those 16 possible lengths
    # and see which one gives us the most legible message
    low, high = possible_prefix_lengths()
    for i in range(low, high):
        print(decrypt_ecb_with_oracle(encryption_oracle, i))
