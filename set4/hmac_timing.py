from flask import Flask
app = Flask(__name__)
from flask import request
import time
from random import randrange
import hashlib
from set1.xor import xor


key = bytes([randrange(255) for _ in range(64)])

def hmac(key, msg):
    """
    https: // en.wikipedia.org / wiki / HMAC
    sha256 is SHA-2
    """
    sha2_block_size, sha2_output_size = 64, 32
    if len(key) > sha2_block_size:
        key = hashlib.sha256().update(key).digest()
    if len(key) < sha2_block_size:
        key = key + bytes([0]*(sha2_block_size - len(key)))
    o_key_pad = xor(key, bytes([0x5c] * sha2_block_size))
    i_key_pad = xor(key, bytes([0x36]* sha2_block_size))
    h1 = hashlib.sha256(i_key_pad + msg).digest()
    return hashlib.sha256(o_key_pad + h1).digest()

def insecure_compare(real_sig, sig, sleep):
    if len(real_sig) != len(sig):
        return "invalid sig", 500
    for (b1, b2) in zip(real_sig, sig):
        if b1 != b2:
            return "invalid sig", 500
        time.sleep(sleep)
    return "valid", 200

@app.route('/test')
def hello_world():
    if "file" not in request.args or "signature" not in request.args:
        return "missing args"
    try:
        sig = bytes.fromhex(request.args["signature"])
    except:
        return "non-hex sig"
    real_sig = hmac(key, bytes(request.args["file"], 'utf-8'))
    print("real, sig", real_sig.hex())
    return insecure_compare(real_sig, sig, 0.05)

def break_insecure_compare(real_sig):
    test_sig = bytearray([0]*32)
    threshold = 40 * 10**6 # 40M ns
    prev_time = 0
    for i in range(32):
        found = False
        for j in range(255):
            # time the compare
            #print(i, j)
            test_sig[i] = j
            start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
            _, code = insecure_compare(real_sig, test_sig, 0.05)
            stop = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
            if code == 200:
                return test_sig
            #print(stop - start, prev_time + threshold)
            if (stop - start) > (prev_time + threshold):
                print("sig byte {} is {}".format(i, j))
                prev_time = stop - start
                found = True
                break
        if not found:
            raise Exception("couldn't find byte", i)
    return test_sig

def find_byte(real_sig, known_sig, sleep):
    from collections import defaultdict
    runtimes = defaultdict(int)
    trials = 10
    for j in range(trials):
        for i in range(255):
            test_sig = known_sig + bytes([i]) + bytes([0]*(32 - len(known_sig)-1))
            start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
            insecure_compare(real_sig, test_sig, sleep)
            stop = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
            runtimes[i] += (stop-start)
    # key where runtime is max
    return sorted([(k, v) for (k, v) in runtimes.items()], key=lambda d: d[1], reverse=True)[0][0]

def break_insecure_compare2(real_sig):
    # With a much smaller time delay there can be noise
    # in program execution times which destroys our
    # thresholding approach.
    # We just need to run it a few times
    # and sum the runtime results to magnify the time differential.
    sig_bytes = b""
    for i in range(32):
        b = bytes([find_byte(real_sig, sig_bytes, 0.005)])
        print(b)
        sig_bytes += b
    return sig_bytes

if __name__ == '__main__':
    # To exploit the timing leak, we try all possible values
    # for a byte, when we notice a spike in processing time we
    # know we've found the correct byte so we proceed to the next one
    # Takes 255 * len(sig) time
    real_sig = hmac(key, b"yellow sub")
    print(real_sig)
    #print(break_insecure_compare(real_sig))
    print(break_insecure_compare2(real_sig))
