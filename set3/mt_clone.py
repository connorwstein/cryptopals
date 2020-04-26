def reverse_right_shift(y2, c):
    """
    Assume y2 = y1 ^ (y1 >> c),
    Return y1

    Take the top c bits and use that
    to uncover the remaining bits, in chunks of c
    Repeat until num_bits - x*c = 0.
    """
    num_bits = len(bin(y2)) - 2
    if num_bits % 2 == 0:
        num_bits += 1
    top_c_bits = y2 >> (num_bits - c)
    bits = bin(top_c_bits)
    rem = num_bits - c
    while rem > 0:
        rem -= c
        next_c_bits = top_c_bits ^ ((y2 >> rem) & (2**(c) - 1))
        bits += bin(next_c_bits)[2:].zfill(c)
        top_c_bits = next_c_bits
    return int(bits,2)

def reverse_left_shift(y2, c1, c2):
    """
    Assume y2 = y1 ^ ((y1 << c1) & c2)
    Return y1

    We know that the last c1 bits will be preserved, because
    (y1 << c1) produces c1 trailing zeroes which when &'d with c2
    produce c1 zeroes, and then ^'d with y1 preserves the trailing c1 bits
    from y1. After that we follow a similar process to the right shift reversal
    but in the other direction.
    """
    num_bits = len(bin(y2)) - 2
    if num_bits % 2 == 0:
        num_bits += 1
    bottom_c1_bits = y2 & (2**(c1) - 1)
    bits = bin(bottom_c1_bits)[2:].zfill(c1)
    rem = num_bits - c1
    while rem > 0:
        part_c2 = c2 >> (num_bits - rem) & (2**(c1) - 1)
        y2_part = (y2 >> (num_bits - rem)) & (2**(c1) - 1)
        next_c1_bits = y2_part ^ part_c2
        bits = bin(next_c1_bits)[2:].zfill(c1) + bits
        bottom_c1_bits = next_c1_bits
        rem -= c1
    return int(bits, 2)


def untemper(output, l, s, t, b, c, u):
    """
    Given a 32bit output from the RNG, untemper that back into
    the corresponding element of the state array
    """
    # if self.index == self.n:
    #     self.twist()
    # y = self.MT[self.index]
    # y = y ^ ((y >> self.u) # note the & self.d doesn't do anythgin
    # y = y ^ ((y << self.s) & self.b)
    # y = y ^ ((y << self.t) & self.c)
    # y = y ^ (y >> self.l)
    # self.index += 1

    # Do the opposite of above
    output = reverse_right_shift(output, 18)
    output = reverse_left_shift(output, 15, int.from_bytes(bytes.fromhex("EFC60000"), byteorder='big'))
    output = reverse_left_shift(output, 7, int.from_bytes(bytes.fromhex("9D2C5680"), byteorder='big'))
    return reverse_right_shift(output, 11)

if __name__ == "__main__":
    a = 10 ^ (10 >> 2)
    print(reverse_right_shift(8, 2))
    a = 54 ^ (52 >> 2)
    print(reverse_right_shift(59, 2))
    a = 1123123 ^ (1123123 >> 7)
    print(reverse_right_shift(a, 7))
    a =  22 ^ ((22 << 2) & 27)
    print(reverse_left_shift(a, 2, 27)) # 22





