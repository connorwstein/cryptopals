from set4.sha1 import sha1
from random import randrange
key = bytes([randrange(255) for _ in range(16)])

def mac(msg):
    return sha1(key + msg)

if __name__ == "__main__":
    print(mac(b"yellow sub"))
    print(mac(b"yellow sub2"))
