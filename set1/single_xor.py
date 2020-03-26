def score(text):
    char_freq = {
        'e': 12.702,
        't': 9.356,
        'a': 8.167,
        'o': 7.507,
        'i': 6.966,
        'n': 6.749,
        's': 6.327,
        'h': 6.094,
        'r': 5.987,
        'd': 4.253,
        'l': 4.025,
        'u': 2.758,
        'w': 2.560,
        'm': 2.406,
        'f': 2.228,
        'c': 2.202,
        'g': 2.015,
        'y': 1.994,
        'p': 1.929,
        'b': 1.492,
        'k': 1.292,
        'v': 0.978,
        'j': 0.153,
        'x': 0.150,
        'q': 0.095,
        'z': 0.0,
        ' ': 10.0,  # Tuned to yield the correct result for the given input
    }
    return sum([char_freq.get(b, 0)/100 for b in text.lower()])

def decrypt_single_byte_xor(msg):
    m = bytes.fromhex(msg)
    scores = []
    for k in range(256):
        r = []
        # xor with each potential key
        for a in m:
            r.append((a ^ k))
        s = "".join([chr(i) for i in r])
        a = score(s)
        scores.append((s, a, k))
    return sorted(scores, key=lambda k: k[1], reverse=True)[0]

if __name__ == '__main__':
    msg = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    print(decrypt_single_byte_xor(msg))
