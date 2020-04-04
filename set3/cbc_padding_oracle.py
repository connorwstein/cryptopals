from random import choice, randrange
from set2.pkcs_padding import unpad_pkcs7
from set2.pkcs_padding_validation import valid_pkcs7_padding
from set2.cbc_mode import encrypt_aes_cbc, decrypt_aes_cbc

key = bytes([randrange(255) for _ in range(16)])
iv = bytes([randrange(255) for _ in range(16)])
import base64

def oracle():
    options = [b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
               b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
               b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
               b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
               b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
               b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
               b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
               b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
               b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
               b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']
    # print([base64.decodebytes(options[i]) for i in range(len(options))])
    return encrypt_aes_cbc(key, choice(options), 16, iv), iv

def check_padding(ct, iv):
    pt = decrypt_aes_cbc(key, ct, 16, iv)
    return valid_pkcs7_padding(pt, 16)

def decrypt_byte_helper(c1, c2, known):
    # take in 2 blocks
    # and learns the byte just before the list of known bytes
    possible_bytes = []
    for i in range(255):
        ct_mut = bytearray(c1)
        pad = len(known) + 1
        # Set pad
        for j, known_byte in enumerate(known):
            ct_mut[-(j+1)] = ct_mut[-(j+1)]^known_byte^pad
        # New byte to try
        ct_mut[-pad] = ct_mut[-pad]^i
        if check_padding(c2, ct_mut):
            possible_bytes.append(i^pad)
    return possible_bytes

def decrypt_byte(c1, c2, known):
    candidates = decrypt_byte_helper(c1, c2, known)
    if len(candidates) == 1 or len(known) == 15:
        return candidates[0]
    for c in candidates:
        a = decrypt_byte_helper(c1, c2, [c] + known)
        if len(a) > 0:
            return c
    raise Exception("could not resolve")

def decrypt_block(c1, c2):
    # returns the decryption of c2
    pt = []
    for i in range(16):
        pt.append(decrypt_byte(c1, c2, pt))
    return bytes(reversed(pt))

if __name__ == '__main__':
    ct, iv = oracle()
    # Goal is to decrypt the set of cipher texts by calling the check padding function
    # on tampered cipher texts.
    ct_blocks = [ct[i*16:(i+1)*16] for i in range(len(ct)//16)]
    print(len(ct_blocks))
    pt = b""
    pt += decrypt_block(iv, ct_blocks[0])
    for i in range(len(ct_blocks)-1):
        pt += decrypt_block(ct_blocks[i], ct_blocks[i+1])
    print(base64.decodebytes(unpad_pkcs7(pt)))




