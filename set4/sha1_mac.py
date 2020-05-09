import set4.sha1 as sha1
from random import randrange
import struct
key = bytes([randrange(255) for _ in range(16)])

def mac(msg):
    return sha1.sha1(key + msg)

def md_padding(msg):
    # padding should be whatever we need
    # to get the total message size to 64 bytes
    len_original = len(msg)
    _, rem = divmod(len_original, 64)
    return b'\x80' + bytes([0]*(64 - rem - 1 - 8)) + struct.pack(b'>Q', len_original*8)

if __name__ == "__main__":
    original = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    to_forge = mac(original)
    to_forge = bytes.fromhex(to_forge)
    regs = [to_forge[i:i+4] for i in range(0, len(to_forge), 4)]
    regs = [int.from_bytes(reg, "big") for reg in regs]
    a,b,c,d,e = regs[0], regs[1], regs[2], regs[3], regs[4]
    key_length_guess = 16
    sh = sha1.Sha1Hash()
    sh._h = (a,b,c,d,e)
    new_text = b";admin=true"
    glue_pad = md_padding(bytes([0]*key_length_guess) + original)
    sh._message_byte_length = len(bytes([0]*key_length_guess) + original + glue_pad)
    if sh.update(new_text).hexdigest() == mac(original + glue_pad + new_text):
        print("forged!", mac(original + glue_pad + new_text))
