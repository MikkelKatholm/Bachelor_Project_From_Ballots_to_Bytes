import sympy as sp
import random
from main import div_mod
import gmpy2 as gmp

def exp_mod(base, exp, mod):
    return pow(base, exp, mod)


def get_prime(bits):
    return sp.randprime(2**(bits-1), 2**bits)

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
    p = get_prime(bits)
    g = find_primitive_root(p)
    g = exp_mod(g, 2, p)
    sk = random.SystemRandom().randint(1,p-1)
    pk = exp_mod(g, sk, p)
    return (p, g, pk, sk)

def encrypt(pk,m,p,g):
    r = random.SystemRandom().randint(1,p-1)
    c1 = exp_mod(g,r,p)
    c2 = (exp_mod(pk,r,p) * exp_mod(g,m,p)) % p
    return (c1,c2)

def decrypt(sk,g,c,p):
    c1,c2 = c
    x = exp_mod(c1,sk,p)
    print(f"x: {x}")
    gm = div_mod(c2,x,p) % p

    possible_m = [i for i in range(0,2)]
    for m in possible_m:
        modm = exp_mod(g,m,p)
        print(f"modm: {modm} \ngm: {gm}")
        if exp_mod(g,m,p) == gm:
            return m
    raise Exception("Decryption failed")

def main():
    p, g, pk, sk = gen_keys(bits)
    print(f"p: {p} \ng: {g} \npk: {pk} \nsk: {sk}")
    m = 0 # Message to encrypt
    c = encrypt(pk,m,p,g)
    c1,c2 = c
    print(f"c1: {c1} \nc2: {c2}")
    print(decrypt(sk,g,c,p))

import random
import sympy

def generate_large_safe_prime(bit_length):
    while True:
        # Generate a random prime number of desired length
        prime_candidate = sympy.randprime(2**(bit_length-1), 2**bit_length)
        
        # Check if the prime candidate is safe
        if sympy.isprime((prime_candidate - 1) // 2):
            return prime_candidate

def test_generate_large_safe_prime():
    bit_length = 128  # Adjust the bit length as per your requirement
    safe_prime = generate_large_safe_prime(bit_length)
    print("Generated Safe Prime:", safe_prime)


def whatthefuck():
    sum_ = gmp.mpz()
    share1 = 932
    sums = gmp.add(sum_, share1)
    print(f"sums: {sums}")

if __name__ == "__main__":
    # set the seed for the random number generator
    whatthefuck()