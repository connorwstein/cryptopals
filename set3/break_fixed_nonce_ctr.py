import base64
from random import randrange
from set1.xor import xor
from set1.single_xor import decrypt_single_byte_xor
from set3.ctr_mode import encrypt_ctr
from collections import defaultdict


def best_k(cts, byte):
    counts = defaultdict(int)
    for i in range(255):
        for ct in cts:
            if byte >= len(ct):
                continue
            pt_byte = ct[byte]^i
            if ord('a') < pt_byte< ord('z') or pt_byte in map(ord, ['.',',',':',';',' ']):
                counts[i] +=1
    return sorted([(k, v) for k, v in counts.items()], reverse=True, key=lambda k:k[1])[0][0]


def approach2(cts):
    # Break this exactly like a repeating xor
    # Concatenate the first byte from every
    key = b""
    for i in range(min([len(c) for c in cts])):
        b = bytes(list(map(lambda x: x[i], cts)))
        _, _, k = decrypt_single_byte_xor(bytes.hex(b))
        key += bytes([k])
    return [xor(key, c[:len(key)]) for c in cts]

if __name__ == "__main__":
    inputs = [
        "SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==",
        "Q29taW5nIHdpdGggdml2aWQgZmFjZXM=",
        "RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==",
        "RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=",
        "SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk",
        "T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        "T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=",
        "UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        "QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=",
        "T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl",
        "VG8gcGxlYXNlIGEgY29tcGFuaW9u",
        "QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==",
        "QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=",
        "QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==",
        "QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=",
        "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=",
        "VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==",
        "SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==",
        "SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==",
        "VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==",
        "V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==",
        "V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==",
        "U2hlIHJvZGUgdG8gaGFycmllcnM/",
        "VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=",
        "QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=",
        "VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=",
        "V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=",
        "SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==",
        "U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==",
        "U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=",
        "VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==",
        "QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu",
        "SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=",
        "VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs",
        "WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=",
        "SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0",
        "SW4gdGhlIGNhc3VhbCBjb21lZHk7",
        "SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=",
        "VHJhbnNmb3JtZWQgdXR0ZXJseTo=",
        "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="]
    # Because we re-used the nonce in CTR mode, we should be able to
    # break all these ciphertexts.
    k = bytes([randrange(255) for _ in range(16)])
    pts = [base64.decodebytes(bytes(i, 'utf-8')) for i in inputs]
    print(pts)
    cts = [encrypt_ctr(base64.decodebytes(bytes(i, 'utf-8')), k, 0) for i in inputs]
    # Try all possible 255 bytes for the first byte of the keystream
    # and xor it with the first byte of every cipher text. If thats an ascii character or space
    # then its very likely to be the keybyte.
    common_key = b""
    for i in range(max([len(c) for c in cts])):
        common_key+=bytes([best_k(cts, i)])
    print(common_key)
    for c in cts:
        print(str(xor(common_key[:len(c)], c), 'utf-8'))

    with open('20.txt') as f:
        cts = [encrypt_ctr(base64.decodebytes(bytes(i, 'utf-8')), k, 0) for i in f.readlines()]
        for p in approach2(cts):
            print(p)
