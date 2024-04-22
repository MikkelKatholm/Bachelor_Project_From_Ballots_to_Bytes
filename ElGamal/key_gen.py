import sympy as sp
import random

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
    p = get_prime(bits)
    q = (p-1)//2
    g = find_primitive_root(p)
    g = exp_mod(g, 2, p)
    sk = random.SystemRandom().randint(1,q-1)
    pk = exp_mod(g, sk, p)
    return (p, q, g, pk, sk)