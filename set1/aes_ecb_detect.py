from collections import defaultdict

# One of the ciphertexts has been encoded with ECB, find it.
# ECB is stateless and deterministic. The same 16 byte plaintext will produce the
# Same 16 byte cipher text.
# We don't know what the key is or if the underlying pt is english.
# We'd expect the determinisim to lead to repeats - lets look for that.
def find_ecb_ct(cipher_texts):
    ecb = None
    most_repeat = 0
    for c in cipher_texts:
        counts_c = defaultdict(int)
        i = 0
        while i < len(c)/16:
            counts_c[c[i*16:(i+1)*16]]+=1
            i += 1
        repeat = max(sorted(counts_c.values(), reverse=True))
        if repeat > most_repeat:
            most_repeat = repeat
            ecb = c
    return ecb, most_repeat
with open('8.txt') as f:
    cipher_texts = [bytes.fromhex(l) for l in f]
print(find_ecb_ct(cipher_texts))
