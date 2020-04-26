from set3.mersenne_twister import MersenneTwister

def reverse_right_shift(y2, c):
    """
    Assume y2 = y1 ^ (y1 >> c),
    Return y1

    Take the top c bits and use that
    to uncover the remaining bits, in chunks of c.
    """
    num_bits = len(bin(y2)) - 2
    num, rem = divmod(num_bits, c)
    i = 2
    # print(num, rem)
    bits = bin(y2 >> (num_bits - c))
    # print(bits)
    while i <= num:
        # Chunks of c
        shift = num_bits - (i * c)
        next = (y2 >> shift) & (2**c - 1)
        # print(next, bits[-c:], bin(next ^ int(bits[-c:], 2))[2:].zfill(c))
        bits += bin(next ^ int(bits[-c:], 2))[2:].zfill(c)
        i += 1
    # Handle remainder
    # Don't need to shift
    if rem != 0:
        next = y2 & (2**rem - 1)
        # print("last", next, bits[-c:(-c+rem)])
        bits += bin(next ^ int(bits[-c:(-c+rem)], 2))[2:].zfill(rem)
    return int(bits, 2)

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
    num, rem = divmod(num_bits, c1)
    i = 1
    # print(num, rem)
    last_found = y2 & (2**c1 - 1)
    bits = bin(last_found)[2:].zfill(c1)
    # print("start", bits)
    while i <= num:
        shift = i * c1
        and_mask = c2 >> shift & (2**c1 - 1)
        to_xor = y2 >> shift & (2**c1 - 1)
        next = (and_mask & last_found) ^ to_xor
        last_found = next
        # print("next", bin(next), bin(and_mask), bin(to_xor))
        bits = bin(next)[2:].zfill(c1) + bits
        i += 1
    return int(bits, 2)


def untemper(output):
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

def temper(input):
    y = input
    y = y ^ ((y >> 11) )
    y = y ^ ((y << 7) & int.from_bytes(bytes.fromhex("9D2C5680"), byteorder='big'))
    y = y ^ ((y << 15) & int.from_bytes(bytes.fromhex("EFC60000"), byteorder='big'))
    y = y ^ (y >> 18)
    return y


if __name__ == "__main__":
    assert(reverse_right_shift(12039131239123 ^ (12039131239123 >> 13), 13))
    assert(reverse_left_shift(1029380129830 ^ ((1029380129830 << 8) & 123), 8, 123) == 1029380129830)
    assert(2000 == untemper(temper(2000)))

    mt = MersenneTwister(2000)
    # mt.extract_random_number()
    numbers = [0]*624
    for i in range(624):
        numbers[i] = mt.extract_random_number()
    state = [0]*624
    for i in range(624):
        state[i] = untemper(numbers[i])
        if state[i] != mt.MT[i]:
            print("bad state", state[i], mt.MT[i])
    mt_clone = MersenneTwister(0)
    mt_clone.MT = state
    for i in range(100):
        c = mt_clone.extract_random_number()
        r = mt.extract_random_number()
        if r != c:
            print(i, r, c)
        # assert(mt_clone.extract_random_number() == mt.extract_random_number())







