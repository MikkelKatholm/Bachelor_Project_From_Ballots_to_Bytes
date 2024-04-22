import sys
sys.path.append("../")
import random
import Shamir.main as shamir
from key_gen import *




""" 
Encrypt a message m f 
"""
def encrypt_for_additive(pk,m,p,g):
    r = random.SystemRandom().randint(1,p-1)
    c1 = exp_mod(g,r,p)
    c2 = (exp_mod(pk,r,p) * exp_mod(g,m,p)) % p
    return (c1,c2)

def decrypt_for_additive(sk,g,c,p,numOfVoters):
    c1,c2 = c
    x = exp_mod(c1,sk,p)
    # gm = c2 / x mod p = c2 * x^-1 mod p
    gm = c2 * exp_mod(x,-1,p) % p

    possible_m = [i for i in range(0,numOfVoters+1)]
    for m in possible_m:
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")

def encrypt_for_shamir(pk, m, g, p):
    q = (p-1)//2
    r = random.SystemRandom().randint(1,q-1)
    print(f"r: {r}")
    c1 = exp_mod(g,r,p)
    c2 = (exp_mod(g,m,p) * exp_mod(pk,r,p)) % p
    return (c1,c2)

def generate_key_shares(sk, numOfShares, threshold, q):
    return shamir.split_secrets(sk, numOfShares, threshold, q)

def calculate_di_for_shamir(c1, share, p):
    di = exp_mod(c1, share[1], p)
    return di


def decrypt_for_shamir(shares, c, g, threshold, p):
    q = (p-1)//2
    c1,c2 = c
    xPoints, dis = zip(*shares)

    print(f"dis: {dis}")
    # Lagrange Basis Polynomial use prime q
    lbp = [shamir.lagrange_For_ElGamal(xPoints, i, threshold, q) for i in range(threshold)]
    print(f"lbp: {lbp}")
    
    diPowerLbp = [exp_mod(dis[i], lbp[i], p) for i in range(threshold)]




    print(f"diPowerLbp: {diPowerLbp}")
    d = 1
    for i in range(threshold):
        d *= diPowerLbp[i]
    print(f"d: {d % p}")

    dm1 = exp_mod(d, -1, p)
    print(f"dm1: {dm1}")
    gm = (c2 * dm1) % p

    possible_m = [i for i in range(0,2)]
    for m in possible_m:
        print(f"exp_mod(g,{m},p): {exp_mod(g,m,p)}")
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")
