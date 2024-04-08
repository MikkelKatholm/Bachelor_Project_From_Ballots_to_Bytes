import random
from key_gen import *




def encrypt(pk,m,p,g):
    r = random.SystemRandom().randint(1,p-1)
    c1 = exp_mod(g,r,p)
    c2 = (exp_mod(pk,r,p) * exp_mod(g,m,p)) % p
    return (c1,c2)

def decrypt(sk,g,c,p,numOfVoters):
    c1,c2 = c
    x = exp_mod(c1,sk,p)
    # gm = c2 / x mod p = c2 * x^-1 mod p
    gm = c2 * exp_mod(x,-1,p) % p

    possible_m = [i for i in range(0,numOfVoters+1)]
    for m in possible_m:
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")
