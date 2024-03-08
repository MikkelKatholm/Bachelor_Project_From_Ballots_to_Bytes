import random
from functools import reduce

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

def div_mod(num, den, fieldsize):
    d, x, _ = extended_euclid_gcd(den, fieldsize)
    if d != 1:
        raise ValueError("Denominator must be coprime to fieldsize")
    return (num * x)



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

    # Calculate the product of a list of numbers
    product = lambda vals: reduce(lambda acc, v: acc * v, vals, 1)
    
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
        numerator += div_mod(top , denominators[i], fieldsize)

    resultAtX = (div_mod(numerator, denominator, fieldsize) + fieldsize) % fieldsize
    return resultAtX

"""  
Reconstructs multiple secrets given m data points where:
    secret1 is at x = -numOfSecrets+1, secret2 is at x = -numOfSecrets+2, ..., secretN is at x = 0
"""
def reconstruct_secrets(shares, numOfSecrets, fieldsize):
    # Make a list of points (-numOfSecrets+1, -numOfSecrets+2, ..., 0)
    points = []
    for i in range(-numOfSecrets+1,1):
        points.append(i)
    print(f"points: {points}")

    # Calculate the secrets encoded at the points
    return [ lagrange_interpolate(p, shares, fieldsize) for p in points ]


"""
Detect errors given t data points by reconstructing polynomial and checking if the checkpoint on the polynomial 
"""
def detect_error(dataPoints, checkPoint, fieldsize):
    x = checkPoint[0]
    y = checkPoint[1]
    y_reconstructed = lagrange_interpolate(x, dataPoints, fieldsize)

    return y_reconstructed != y 

