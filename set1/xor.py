def xor(b1, b2):
    return bytes([a ^ b for a,b in zip(b1, b2)])

if __name__ == '__main__':
    print(xor(bytes.fromhex("1c0111001f010100061a024b53535009181c"), bytes.fromhex("686974207468652062756c6c277320657965")).hex())