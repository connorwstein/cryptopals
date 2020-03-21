import itertools
import base64
from set1.single_xor import decrypt_single_byte_xor
from set1.repeate_xor import encrypt_repeating_xor

# Number of differing bits in two bytes


def num_diff_bits(b1, b2):
    num = 0
    while b1 > 0 or b2 > 0:
        num += (b1 & 1) ^ (b2 & 1)
        b1 >>= 1
        b2 >>= 1
    return num

# Return the edit distance between two strings
# the number of differing bits


def edit_distance(s1, s2):
    if len(s1) != len(s2):
        raise Exception("not the same size")
    return sum([num_diff_bits(b1, b2) for b1, b2 in zip(s1, s2)])


assert(edit_distance(bytes("this is a test", 'utf-8'),
                     bytes("wokka wokka!!!", 'utf-8')) == 37)


def find_key_size(ciphertext):
    # Takes in an array of bytes
    # try keysize [2, 40]
    # We just get better results if we average all the blocks
    key_sizes = []
    for key_size in range(2, 41):
        blocks = []
        for i in range(4):
            blocks.append(ciphertext[key_size*i:key_size*(i+1)])
        eds = []
        for comb in itertools.combinations(blocks, 2):
            eds.append(edit_distance(comb[0], comb[1]) / key_size)
        key_sizes.append((key_size, sum(eds)/len(eds)))
    return sorted(key_sizes, key=lambda k: k[1])[0][0]


def break_repeating_xor(file):
    with open(file, 'rb') as f:
        contents = f.read()
    msg = base64.decodebytes(contents)
    key_size = find_key_size(msg)
    # Transpose the bytes into blocks
    # Store our list of blocks as an ordered list of ordered lists
    blocks = [[] for _ in range(key_size)]  # list of bytes
    for i, b in enumerate(msg):
        blocks[i % key_size].append(b)
    key = []
    for block in blocks:
        _, _, key_for_block = decrypt_single_byte_xor(bytes(block).hex())
        key.append(chr(key_for_block))
    decrypted = encrypt_repeating_xor(''.join(key), msg)
    return decrypted.decode('utf-8')


print(break_repeating_xor('6'))
