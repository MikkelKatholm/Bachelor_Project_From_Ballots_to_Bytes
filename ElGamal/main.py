import sys
sys.path.append("../")
import random
import Shamir.main as shamir
import sympy as sp



def exp_mod(base, exp, mod):
    return pow(base, exp, mod)

def get_prime(bits):
    while True:
        # Generate a random prime number of desired length
        prime_candidate = sp.randprime(2**(bits-1), 2**bits)
        # Check if the prime candidate is safe
        if sp.isprime((prime_candidate - 1) // 2):
            return prime_candidate

def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p-1) // p1

    while(1):
        g = random.SystemRandom().randint(2,p-1)
        if not (exp_mod(g, (p-1)//p1, p) == 1):
            if not exp_mod(g, (p-1)//p2, p) == 1:
                return g
            
def gen_keys(bits):
    global p, q, g
    p = get_prime(bits)
    q = (p-1)//2
    g = find_primitive_root(p)
    g = exp_mod(g, 2, p)
    sk = random.SystemRandom().randint(1,q-1)
    pk = exp_mod(g, sk, p)
    return (pk, sk)


def decrypt_for_additive(sk,c,numOfVoters):
    c1,c2 = c
    x = exp_mod(c1,sk,p)
    gm = c2 * exp_mod(x,-1,p) % p

    possible_m = [i for i in range(0,numOfVoters+1)]
    for m in possible_m:
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")

def encrypt(pk, m):
    q = (p-1)//2
    r = random.SystemRandom().randint(1,q-1)
    c1 = exp_mod(g,r,p)
    c2 = (exp_mod(g,m,p) * exp_mod(pk,r,p)) % p
    return (c1,c2)

def generate_key_shares(sk, numOfShares, threshold):
    return shamir.split_secrets(sk, numOfShares, threshold, q)

def calculate_di_for_shamir(c1, share):
    di = exp_mod(c1, share[1], p)
    return di


def decrypt_for_shamir(shares, c, threshold, numOfVoters):
    _,c2 = c
    xPoints, dis = zip(*shares)

    # Lagrange Basis Polynomial use prime q
    lbp = [shamir.lagrange_For_ElGamal(xPoints, i, threshold, q) for i in range(threshold)]
    
    diPowerLbp = [exp_mod(dis[i], lbp[i], p) for i in range(threshold)]

    d = 1
    for i in range(threshold):
        d *= diPowerLbp[i]

    dm1 = exp_mod(d, -1, p)
    gm = (c2 * dm1) % p

    possible_m = [i for i in range(0,numOfVoters+1)]
    for m in possible_m:
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")
