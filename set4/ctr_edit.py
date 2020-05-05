import base64
from random import randrange
from set3.ctr_mode import encrypt_ctr, decrypt_ctr
import copy
from set1.xor import xor
from set1.aes_ecb import decrypt_aes_ecb

def edit(ct, key, offset, newtext):
    # Overwrite ct at offset with encrypted(new_text)
    ct = copy.deepcopy(ct)
    pt = bytearray(decrypt_ctr(ct, key, 0))
    pt[offset:offset+len(newtext)] = newtext
    return encrypt_ctr(bytes(pt), key, 0)

def ctr_edit_decrypt(ct, edit):
    """
    Attacker has an edit function and a ct.
    To recover the plaintext, we xor our
    specified pt with the associated edited ct to get
    E(nonce..counter) for that given block. Then
    E(nonce..counter) ^ original ct gives us the original pt.
    """
    pt = b""
    attacker_pt = bytes([0]*16)
    for i in range(0, len(ct), 16):
        new_ct = edit(ct, i, attacker_pt)
        e = xor(new_ct[i:i+16], attacker_pt)
        pt_block = xor(e, ct[i:i+16])
        pt += pt_block
    return pt

if __name__ == "__main__":
    with open('25.txt', 'rb') as f:
        contents = f.read()
    ct = base64.decodebytes(contents)
    pt_original = decrypt_aes_ecb(b"YELLOW SUBMARINE", ct)
    k = bytes([randrange(255) for _ in range(16)])
    ct = encrypt_ctr(pt_original, k, 0)
    def attacker_edit(ct, offset, newtext):
        return edit(ct, k, offset, newtext)
    pt = ctr_edit_decrypt(ct, attacker_edit)
    assert(pt == pt_original)
