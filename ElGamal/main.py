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

def encrypt_for_shamir(pk,m,p,g):
    r = random.SystemRandom().randint(1,p-1)
    print(f"r: {r}")
    c1 = exp_mod(g,r,p)
    c2 = (exp_mod(g,m,p) * exp_mod(pk,r,p)) % p
    return (c1,c2)

def generate_key_shares(sk, numOfShares, threshold, p):
    return shamir.split_secrets(sk, numOfShares, threshold, p)

def calculate_di_for_shamir(c1, share, p):
    di = exp_mod(c1, share[1], p)
    return di


def decrypt_for_shamir(shares, c, g, threshold, p):
    c1,c2 = c
    dis, xPoints = zip(*shares)

    print(f"dis: {dis}")
    print(f"xPoints: {xPoints}")
    basisPolys = [shamir.lagrange_For_ElGamal(xPoints, i, threshold, p) for i in range(threshold)]  #OK
    print(f"basisPolys: {basisPolys}")

    # Calculate d = prod (di^Li) mod p
    d = 1

    for i in range(threshold):
        d *= exp_mod(dis[i], basisPolys[i], p)
        d = d % p

    
    dexpm1 = exp_mod(d,-1,p)
    gm = (c2 * dexpm1) % p
    print(f"c2*dexpm1: {c2*dexpm1}")
    print(f"d: {d}")
    print(f"dexpm1: {dexpm1}")
    print(f"gm: {gm}")

    possible_m = [i for i in range(0,2)]
    for m in possible_m:
        print(f"exp_mod(g,{m},p): {exp_mod(g,m,p)}")
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")
