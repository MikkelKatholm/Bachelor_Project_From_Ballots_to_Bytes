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
        d, x, y = dp, yp, xp - (a//b)*yp
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
Secrets:    A list of secrets
n:          Number of shares to make
t:          Threshold
fieldsize:  The big prime number to use for the finite field
"""
def split_secrets(secrets, n, t, fieldsize):
    if (n < t):
        raise ValueError("Threshold t must be larger than number of shares n")
    k = len(secrets)

    pointsForPoly = []
    pointsForShares = [ i for i in range(1+t,n+1+t) ]
    coefficients = [random.SystemRandom().randint(0,fieldsize-1) for _ in range(t-1)]
    print("Coefficients: ", coefficients)
    
    # Make a list of points where (-len(secrets), f(-len(secrets))), (-len(secrets)+1, f(-len(secrets)+1)), ..., (0, f(0)
    for i in range(-k, 0+t-1):
        pointsForPoly.append((i+1))

    values = secrets + coefficients

    polynomial = list(zip(pointsForPoly, values))

    shares = [ (p,lagrange_interpolate(p, polynomial, fieldsize)) for p in pointsForShares]
    return shares



"""
Given m data points and x, interpolate the polynomial and return f(x)
"""
def lagrange_interpolate(x, datapoints, fieldsize):
    x_points, y_points = zip(*datapoints)

    numOfPoints = len(x_points)

    def product(vals):
        acc = 1
        for v in vals:
            acc *= v
        return acc
    
    denominators = []
    numerators = []
    for i in range(numOfPoints):
        restOfList = list(x_points)
        working_x = restOfList.pop(i)
        numsList = (x - o for o in restOfList)
        densList = (working_x - o for o in restOfList)
        numerators.append(product(numsList))
        denominators.append(product(densList))
    denominator = product(denominators)
    numerator = 0
    for i in range(numOfPoints):
        top = y_points[i] * (numerators[i] * denominator) % fieldsize
        numerator += divMod(top , denominators[i], fieldsize)

    resultAtX = (divMod(numerator, denominator, fieldsize) + fieldsize) % fieldsize
    return resultAtX


def reconstruct_multiple_secrets(shares, numOfSecrets, fieldsize):
    # Make a list of points (-numOfSecrets+1, -numOfSecrets+2, ..., 0)
    points = []
    for i in range(-numOfSecrets+1,1):
        points.append(i)

    # Calculate the secrets encoded at the points
    return [ lagrange_interpolate(p, shares, fieldsize) for p in points ]


"""
Detect errors given t data points by reconstructing polynomial and checking if the checkpoint on the polynomial 
"""
def detectError(dataPoints, checkPoint, fieldsize):
    x = checkPoint[0]
    y = checkPoint[1]
    y_reconstructed = lagrange_interpolate(x, dataPoints, fieldsize)

    return y_reconstructed != y 

# Secret, number of shares n, threshold t
# 1) Split secret into shares: 
    # Make polynomial of degree t-1, where f(0) = secret
    # Make n data points (x, f(x)), with x = 1, 2, ..., n
# 2) Send shares 
# 3) Reconstruct secret with Lagrange interpolation
def main():
    secret = 1001
    numOfShares = 6
    threshold = 3
    fieldsize = 2**127 - 1

    shares = split_secret(secret, numOfShares, threshold, fieldsize)

    reconstructedSecret = lagrange_interpolate(0, shares[:3], threshold, fieldsize)
    print("Reconstructed secret: ", reconstructedSecret)

    assert secret == reconstructedSecret, "Secrets do not match"
    