from set3.mersenne_twister import MersenneTwister
import random

def encrypt(key, msg):
    m = MersenneTwister(key)
    i = 0
    r = m.extract_random_number()
    current_key = r.to_bytes(4, 'big')
    print(m.MT[0], m.MT[2], r)
    ct = bytearray([])
    for byte in msg:
        if i != 0 and i % 4 == 0:
            current_key = m.extract_random_number().to_bytes(4, 'big')
        ct.append(current_key[i] ^ byte)
        i= (i + 1) % 4
    return bytes(ct)

if __name__ == '__main__':
    random_prefix = bytearray([random.randrange(255) for i in range(random.randrange(1, 10))])
    random_prefix += b"AAAAAAAAAAA"
    enc = encrypt(20, random_prefix)
    num, rem = divmod(len(enc), 4)
    if rem == 0:
        a = enc[-4:]
    elif rem == 1:
        a = enc[-5:-1]
    elif rem == 2:
        a = enc[-6:-2]
    elif rem == 3:
        a = enc[-7:-3]
    helper = int.from_bytes([ord('A') ^ int(a[0]), ord('A') ^ int(a[1]), ord('A') ^ int(a[2]), ord('A') ^ int(a[3])], "big")
    found = False
    # The random prefix makes this harder, can't untwist to go back in time
    # Might still be brute forcible depending on the size of the prefix
    for i in range(65536):
        if found:
            break
        mt = MersenneTwister(i)
        for j in range(10):
            if mt.extract_random_number() == helper:
                print("seed", i)
                found = True
                break
