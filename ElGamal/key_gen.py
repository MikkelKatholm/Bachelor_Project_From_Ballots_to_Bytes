import sympy as sp
import random

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