# Mersenne twister is a RNG
# based on a linear feedback shift register LFSR.
# A linear feedback shift register is a shift register where the input bit
# is a linear combination of the state of the register and the seed is the initial
# state of the register.
# Idea is to generate a series X_i, then output numbers of the form x_i * T
# where T is a "tempering matrix"
# GFSR https://dl.acm.org/doi/10.1145/321765.321777
# TGFSR http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/ARTICLES/tgfsr3.pdf

# w = word size, n = degree of recurrence i.e. number of integers in MT array
(w, n) =  (32, 624)
# Seeding parameters
f = 1812433253
# Extracting parameters
(u, d) = (11, int.from_bytes(bytes.fromhex("FFFFFFFF"), byteorder='big'))
(s, b) = (7, int.from_bytes(bytes.fromhex("9D2C5680"), byteorder='big'))
(t, c) = (15, int.from_bytes(bytes.fromhex("EFC60000"), byteorder='big'))
l = 18
# Twisting parameters
# m = offset used in the recurrence relation defining the series
# r = number of bits in the lower bit mask
# a = coefficients of the rational normal form twist matrix?
# lower mask  = 0111...1, upper max = 1000...0
(m, r) = (397, 31)
a = int.from_bytes(bytes.fromhex("9908B0DF"), byteorder='big')
lower_mask = (1<<r)-1
upper_mask=1<<r

# MT = mersenne twister
# The MT array is like an the state of an LFSR
# It stores 624 32bit integers
MT = [0]*n
index = n+1

def seed_mt(seed):
    """
    Populate the initial 624 32-bit ints in the MT array based on the seed.
    Produces [x_0 x_1 ... x_(n-1)]
    Where x_0 = seed
    x_1 = x_0 ^ last 2 bits of x_0 + 1
    x_2 = x_1 ^ last 2 bits of x_1 + 2
    ...
    Why seed like this?
    """
    global index
    index = n
    MT[0] = seed
    for i in range(1, n):
        MT[i] = int_32(f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i)
    print(MT)

def extract_number():
    """
    Creates a value based on MT[index]
    # The xors implement the tempering matrix
    # which represents the linear function
    # which produces the output 32-bit integers
    # based on the state (MT).
    """
    global index
    if index > n:
        raise Exception("unseeded")
    if index == n:
        twist()
    y = MT[index]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    index+=1
    return int_32(y)

def twist():
    """
    Every time the index hits the last of the 624 32-bit numbers, we "twist".
    A twist manipulates the internal state (MT).
    This twisting process changes the GFSR from
        x_(l+n) = x_(l+m)^x_l  (l=0,1,2 and 0<m<n)
        to
        x_(l+n) = x_(l+m)^(x_l*A) (where A is a special twisting matrix)
    The twisting allows us to obtain the maximum period of the PRNG possible (2^nw -1 states),
    rather than 2^n-1 period in a GFSR.
    """
    global index
    for i in range(n):
        x = int_32(MT[i] & upper_mask) + (MT[(i+1) % n] & lower_mask)
        xA = x >> 1
        if (x % 2) != 0:
            xA = xA ^ a
        MT[i] = MT[(i + m) % n] ^ xA
    index = 0

def int_32(number):
    return int(0xFFFFFFFF & number)

if __name__ == '__main__':
    seed_mt(2000)
    for i in range(10):
        print(extract_number())


