from set2.detection_oracle import random_aes_key
from set2.pkcs_padding import pad_pkcs7, unpad_pkcs7
from set1.aes_ecb import  encrypt_aes_ecb, decrypt_aes_ecb
profile_id_seq = 0

def profile_for(email):
    global profile_id_seq
    if '&' in email or '=' in email:
        raise Exception("invalid email")
    profile_id_seq += 1
    profile = {
        "email": email,
        "uid": profile_id_seq,
        "role": "user",
    }
    return '&'.join(["{}={}".format(k, v) for k, v in profile.items()])

def parse_kv(text):
    map = {}
    for item in text.split('&'):
        kv = item.split('=')
        if len(kv) != 2:
            raise Exception("invalid text")
        map[kv[0]] = kv[1]
    # more checks for all required keys
    return map

def encrypt(key, profile):
    return encrypt_aes_ecb(key, pad_pkcs7(bytes(profile, 'utf-8'), 16))

def decrypt(key, ct):
    profile = decrypt_aes_ecb(key, ct)
    print(profile)
    return parse_kv(str(unpad_pkcs7(profile), 'utf-8'))


if __name__ == '__main__':
    print(parse_kv("foo=bar&baz=qux&zap=zazzle"))
    print(profile_for("test@gmail.com"))
    key = random_aes_key()
    print(decrypt(key,encrypt(key, profile_for("test@gmail.com"))))
    # Using only the user input to profile_for()
    # (as an oracle to generate "valid" ciphertexts) and
    # the ciphertexts themselves, make a role=admin profile.

    # Want something that when we decrypt it, we've changed the role to admin
    # in other words we've changed the final few bytes.
    # We know that its adding &uid=X&role=user (15 bytes)
    # 1. Pick an email E such that:
    # email=E&uid=1&role= --> is exactly 32 bytes
    first_two_blocks = encrypt(key, profile_for('A'*14))[:32]
    # 2. Pick an email E such that:
    # email=E is exactly 2 blocks where the second block is |admin+pkcs7 padding|
    last_block = encrypt(key, profile_for("A"*10 + "admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"))[16:32]
    print(decrypt(key, first_two_blocks+last_block))
