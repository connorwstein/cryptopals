from set2.detection_oracle import random_aes_key
from set2.pkcs_padding import pad_pkcs7
from set1.aes_ecb import encrypt_aes_ecb
from set1.aes_ecb_detect import  is_ecb
import base64

key = random_aes_key()

def encryption_oracle(msg):
    secret = base64.decodebytes(bytes(b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' +
                b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
                b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'))
    msg = msg + secret
    return encrypt_aes_ecb(key, pad_pkcs7(msg, 16))

def find_block_size(oracle):
    # Feed 1 byte at a time until we know the block_size. Assuming we don't know
    # the padding scheme, we can just keep adding until we see a jump
    # the jump is the block size.
    start = len(oracle(b'A'))
    current = start
    i = 2
    while start == current:
        current = len(oracle(b'A' * i))
        i += 1
    return current - start

def find_next_byte(oracle, ask, have, bs, block, prefix_length):
    possible_last_bytes = {bytes(have + [i]):oracle(bytes(have +[i])) for i in range(255)}
    enc = oracle(bytes(ask))
    for k, v in possible_last_bytes.items():
        if enc[prefix_length:bs*block] == v[prefix_length:bs*block]:
            return k[-1]
    return -1

def decrypt_ecb_with_oracle(oracle, prefix_length):
    bs = find_block_size(oracle)
    using_ecb = is_ecb(oracle(b'yellow submarine' * 10), bs)
    if not using_ecb:
        raise Exception("can't do this attack")
    decrypted, i = [], prefix_length
    while True:
        block, index_in_block = divmod(i, bs)
        # we want ask be whatever number of bytes that gets us to block_size - 1
        # [D1 D2 D3 D4] [D5 A A S]
        # Each iteration we decrypt one byte, and move that from ask to have
        # prefix + decrypted + A's = block multiple - 1
        # and we compare against
        ask = [ord('A')]*(bs - index_in_block - 1)
        have = ask + decrypted
        secret_byte = find_next_byte(oracle, ask, have, bs, block+1, prefix_length)
        if secret_byte == -1:
            break
        decrypted.append(secret_byte)
        i += 1
    return bytes(decrypted)

if __name__ == '__main__':
    print(decrypt_ecb_with_oracle(encryption_oracle, 0))
