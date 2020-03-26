from collections import Counter

def is_ecb(ct, block_size):
    """Check for repeated ct blocks"""
    return sorted(Counter([ct[i*block_size:(i+1)*block_size] for i in range(len(ct)//block_size)]).values(), reverse=True)[0] > 1

def find_ecb_ct(cipher_texts):
    # One of the ciphertexts has been encoded with ECB, find it.
    # ECB is stateless and deterministic. The same 16 byte plaintext will produce the
    # Same 16 byte cipher text.
    # We don't know what the key is or if the underlying pt is english.
    # We'd expect the determinisim to lead to repeats - lets look for that.
    return any(is_ecb(ct, 16) for ct in cipher_texts)

if __name__ == '__main__':
    with open('8.txt') as f:
        cipher_texts = [bytes.fromhex(l) for l in f]
    print(find_ecb_ct(cipher_texts))
