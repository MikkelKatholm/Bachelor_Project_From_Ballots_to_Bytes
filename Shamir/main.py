import math
import random


""" 
Extended Euclid gcd
Input:      A pair of nonnegative integers a and b.
Output:     A triple (d, x, y) such that d = gcd(a, b) and ax + by = d.
Reference:  Introduction to algorithms, 3rd edition, page 937
Tested:     True
"""
def extended_euclid_gcd(a,b):
    isBothNonNegative = a >= 0 or b >= 0
    if not isBothNonNegative:
        raise ValueError("Both numbers must be non-negative")

    if b == 0:
        return (a,1,0)
    else: 
        dp, xp, yp = extended_euclid_gcd(b, a % b)
        d, x, y = dp, yp, xp - math.floor(a//b)*yp
        return d, x, y
    
def divMod(num, den, fieldsize):
    d, x, _ = extended_euclid_gcd(den, fieldsize)
    if d != 1:
        raise ValueError("Denominator must be coprime to fieldsize")
    return (num * x)


"""
Returns data points (x, f(x)) for splitting up secret
poly:   The polynomial to evaluate at and split secret 
x:      The point to evaluate at
Tested: True
"""
def polynomialValueAtX(poly, x, fieldsize):
    value = 0
    for cof in reversed(poly):
        value *= x
        value += cof
        value %= fieldsize
    return value

""" 
Secret is set to be f(0)
n:  Number of shares to make
t:  Minimum amount of shares that must be pooled to reconstruct secret
"""
def split_secret(secret, n, t, fieldsize):
    if (n < t):
        raise ValueError("Threshold t must be larger than number of shares n")
    # Make polynomial of degree t-1, where f(0) = secret
    coefficients = [secret] + [random.SystemRandom().randint(0,fieldsize-1) for _ in range(t-1)]
    points = []
    for i in range(1, n+1):
        value = polynomialValueAtX(coefficients, i, fieldsize)
        points.append((i, value))
    
    return points

"""
Given t datapoints, construct t basis polynomials
"""
def reconstructSecret(dataPoints, t, fieldsize):
    if len(dataPoints) < t:
        raise ValueError("Not enough data points to make basis polynomials")
    x_points, y_points = zip(*dataPoints)    
    res = 0
    for j in range(t):
        xj = x_points[j]
        temp = 1
        for m in range(t):
            if m != j:
                xm = x_points[m]
                divModRes = divMod(xm,xm-xj,fieldsize)
                temp *= divModRes
                temp %= fieldsize
        temp *= y_points[j]
        temp %= fieldsize
        res += temp
        res %= fieldsize
    return res 

# Secret, number of shares n, threshold t
# 1) Split secret into shares: 
    # Make polynomial of degree t-1, where f(0) = secret
    # Make n data points (x, f(x)), with x = 1, 2, ..., n
# 2) Send shares 
# 3) Reconstruct secret with Lagrange interpolation
def main():
    secret = 1234
    numOfShares = 6
    threshold = 3
    fieldsize = 1619

    shares = split_secret(secret, numOfShares, threshold, fieldsize)

    reconstructedSecret = reconstructSecret(shares[:3], threshold,fieldsize)
    assert secret == reconstructedSecret
    