# Mersenne twister is a RNG
# based on a linear feedback shift register LFSR.
# A linear feedback shift register is a shift register where the input bit
# is a linear combination of the state of the register and the seed is the initial
# state of the register.
# Idea is to generate a series X_i, then output numbers of the form x_i * T
# where T is a "tempering matrix"
# GFSR https://dl.acm.org/doi/10.1145/321765.321777
# TGFSR http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/ARTICLES/tgfsr3.pdf

class MersenneTwister(object):
    def __init__(self, seed):
        # w = word size, n = degree of recurrence i.e. number of integers in MT array
        self.w = 32
        self.n = 624
        # Seeding parameters
        self.f = 1812433253
        # Extracting parameters
        self.u = 11
        self.d = int.from_bytes(bytes.fromhex("FFFFFFFF"), byteorder='big')
        self.s = 7
        self.b = int.from_bytes(bytes.fromhex("9D2C5680"), byteorder='big')
        self.t = 15
        self.c = int.from_bytes(bytes.fromhex("EFC60000"), byteorder='big')
        self.l = 18
        # Twisting parameters
        # m = offset used in the recurrence relation defining the series
        # r = number of bits in the lower bit mask
        # a = coefficients of the rational normal form twist matrix?
        # lower mask  = 0111...1, upper max = 1000...0
        self.m = 397
        self.r = 31
        self.a = int.from_bytes(bytes.fromhex("9908B0DF"), byteorder='big')
        self.lower_mask = (1<<self.r)-1
        self.upper_mask=1<< self.r

        # MT = mersenne twister
        # The MT array is like an the state of an LFSR
        # It stores 624 32bit integers
        self.MT = [0]*self.n
        self.index = self.n+1
        self.seed_mt(seed)

    def seed_mt(self, seed):
        """
        Populate the initial 624 32-bit ints in the MT array based on the seed.
        Produces [x_0 x_1 ... x_(n-1)]
        Where x_0 = seed
        x_1 = x_0 ^ last 2 bits of x_0 + 1
        x_2 = x_1 ^ last 2 bits of x_1 + 2
        ...
        Why seed like this?
        """
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = self.int_32(self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i)

    def extract_random_number(self):
        """
        Creates a value based on MT[index]
        # The xors implement the tempering matrix
        # which represents the linear function
        # which produces the output 32-bit integers
        # based on the state (MT).
        """
        if self.index > self.n:
            raise Exception("unseeded")
        if self.index == self.n:
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index+=1
        return self.int_32(y)

    def twist(self):
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
        for i in range(self.n):
            x = self.int_32(self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def int_32(self, number):
        return int(0xFFFFFFFF & number)

if __name__ == '__main__':
    mt = MersenneTwister(2000)
    for i in range(10):
        print(mt.extract_random_number())


