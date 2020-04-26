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
    bits = bin(y2 >> (num_bits - c))
    while i <= num:
        # Chunks of c
        shift = num_bits - (i * c)
        next = (y2 >> shift) & (2**c - 1)
        bits += bin(next ^ int(bits[-c:], 2))[2:].zfill(c)
        i += 1
    # Handle remainder
    # Don't need to shift
    if rem != 0:
        next = y2 & (2**rem - 1)
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
    num, rem = divmod(32, c1)
    i = 1
    last_found = y2 & (2**c1 - 1)
    bits = bin(last_found)[2:].zfill(c1)
    while i < num:
        shift = i * c1
        and_mask = c2 >> shift & (2**c1 - 1)
        to_xor = y2 >> shift & (2**c1 - 1)
        next = (and_mask & last_found) ^ to_xor
        last_found = next
        bits = bin(next)[2:].zfill(c1) + bits
        i += 1
    if rem != 0:
        shift = 32 - rem
        and_mask = c2 >> shift & (2**rem - 1)
        to_xor = y2 >> shift & (2**rem - 1)
        next = and_mask & int(bits[c1-rem:c1], 2) ^ to_xor
        bits = bin(next)[2:].zfill(rem) + bits
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
    assert(2000 == untemper(temper(2000)))
    assert(2381658102 == untemper(temper(2381658102)))

    mt = MersenneTwister(2000)
    numbers = [0]*624
    for i in range(624):
        numbers[i] = mt.extract_random_number()
    state = [0]*624
    for i in range(624):
        state[i] = untemper(numbers[i])
    mt_clone = MersenneTwister(0)
    mt_clone.MT = state
    for i in range(100):
        c = mt_clone.extract_random_number()
        r = mt.extract_random_number()
        assert(mt_clone.extract_random_number() == mt.extract_random_number())
