iceice = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
# Encrypt repeating xor key is a byte array


def encrypt_repeating_xor(key, msg):
    curr = 0
    result = bytearray()
    for b in msg:
        result.append(b ^ ord(key[curr % len(key)]))
        curr += 1
    return result


print(encrypt_repeating_xor("ICE", bytes(iceice, 'utf-8')).hex())
