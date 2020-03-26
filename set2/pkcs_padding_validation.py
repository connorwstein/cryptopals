def valid_pkcs7_padding(input, block_size):
    last_byte = input[-1]
    return len(input) % block_size == 0 and all([last_byte == i for i in input[-last_byte:]])

if __name__ == '__main__':
    print(valid_pkcs7_padding(b"ICE ICE BABY\x04\x04\x04\x04", 16))
    print(valid_pkcs7_padding(b"ICE ICE BABY\x05\x05\x05\x05", 16))
    print(valid_pkcs7_padding(b"ICE ICE BABY\x01\x02\x03\x04", 16))
