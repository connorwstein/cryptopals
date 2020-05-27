from random import randint
from random import seed
import time
from set2.cbc_mode import encrypt_aes_cbc, decrypt_aes_cbc
import set4.sha1 as sha1

class DiffieUser(object):
    def __init__(self, g, p, mitm=False):
        """
        :param p: prime
        :param g: generator
        """
        self.mitm = mitm
        self.p = p
        self.g = g
        self.a, self.A, self.B, self.key = None, None, None, None

    def __repr__(self):
        return "p {} a {} A {} B {} key {}".format(self.p, self.a, self.A, self.B, self.key)

    def send_params(self, UserB):
        if self.p is None or self.g is None:
            raise Exception("need params p and g")
        # Choose my secret if I havent already
        if self.a is None:
            seed(time.time_ns())
            self.a = randint(0, self.p)
            self.A = (self.g ** self.a) % self.p
        if self.mitm:
            UserB.recv_params(self.g, self.p, self.p)
        else:
            UserB.recv_params(self.g, self.p, self.A)

    def recv_params(self, g, p, B):
        # Obtain the other half from partner
        # Generate session key
        self.g = g
        self.p = p
        self.B = B
        if self.a is None:
            seed(time.time_ns())
            self.a = randint(0, self.p)
            self.A = (self.g ** self.a) % self.p
        self.key = ((B ** self.a) % self.p).to_bytes(192, "big")

    def send_share(self, UserB):
        if self.A is None:
            raise Exception("need share")
        if self.mitm:
            UserB.recv_share(self.p)
        else:
            UserB.recv_share(self.A)

    def recv_share(self, B):
        if self.B is None:
            self.B = B
        if self.a is None:
            seed(time.time_ns())
            self.a = randint(0, self.p)
        self.key = ((self.B ** self.a) % self.p).to_bytes(192, "big")

    def send(self, msg, UserB):
        riv = bytes([randint(0, 255) for _ in range(16)])
        UserB.recv(encrypt_aes_cbc(sha1.Sha1Hash().update(self.key).digest()[:16], msg, 16, riv) + riv)

    def recv(self, msg):
        if self.mitm:
            # If we are the MITM we know that B = p
            # so the key is p^a mod p = 0
            pt = decrypt_aes_cbc(sha1.Sha1Hash().update(int(0).to_bytes(192, "big")).digest()[:16], msg[:-16], 16, msg[-16:])
            print("mitm received", pt)
        else:
            pt = decrypt_aes_cbc(sha1.Sha1Hash().update(self.key).digest()[:16], msg[:-16], 16, msg[-16:])
            print("received", pt)


if __name__ == "__main__":
    userA = DiffieUser(0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff, 3761)
    userB = DiffieUser(None, None)
    userA.send_params(userB)
    userB.send_share(userA)
    print("User A", userA)
    print("User B", userB)

    userA.send(b"hello world", userB)


    # MITM attack
    userA = DiffieUser(0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff, 3761)
    userM = DiffieUser(None, None, mitm=True)
    userB = DiffieUser(None, None)

    # A->M params
    userA.send_params(userM)
    # M->B params'
    userM.send_params(userB)
    # B->M B
    userB.send_share(userM)
    # M->A p
    userM.send_share(userA)
    print("User A", userA)
    print("User M", userM)
    print("User B", userB)
    userA.send(b"hello world", userM)
