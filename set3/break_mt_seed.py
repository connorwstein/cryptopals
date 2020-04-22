from set3.mersenne_twister import MersenneTwister
from random import randrange
import time

def output():
    time.sleep(randrange(40, 1000))
    seed = int(time.time())
    print("Using seed:", seed)
    mt = MersenneTwister(seed)
    # Return the first 32bit output of the number
    return mt.extract_random_number()

def crack(output):
    # Brute force possible timestamp seeds
    current = int(time.time())
    for i in range(100000):
        guess = MersenneTwister(current-i).extract_random_number()
        if guess == output:
            return current-i
    raise Exception("couldn't crack")

if __name__ == '__main__':
    a = output()
    print("Seed used was: ", crack(a))
