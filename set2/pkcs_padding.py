# bytes is immutable, bytearray is mutable
def pad_pkcs7(pt, block_size):
    # 01, 02, 02...
    # if the message equals a multiple of the block_size then we
    # add a full block of padding
    if len(pt) % block_size == 0:
        return bytes(pt + bytes([block_size for _ in range(block_size)]))
    pad = block_size - len(pt) % block_size
    return bytes(pt + bytes([pad for _ in range(pad)]))

print(pad_pkcs7(bytes("YELLOW SUBMARINE", 'utf-8'), 20))