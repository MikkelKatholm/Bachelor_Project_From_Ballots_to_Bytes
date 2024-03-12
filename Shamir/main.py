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

def berlekamp_welsh(shares, maxNumOfErrors, finalDegree, fieldsize):
    import sympy as sp
    k = maxNumOfErrors 
    n = finalDegree 
    n2k = n + 2*k 
    nk = n + k 
    xp, yp = zip(*shares)
    # A matrix of size n2k x nk (rows x columns)
    A = sp.zeros(n2k, nk)
    for i in range(n2k):
        for j in range(nk):
            A[i,j] = (xp[i])**j
    
    # Flip the matrix so the largest coefficients are first in each row
    A = sp.Matrix(A[:,::-1])
    # b Matrix of size n2k x k+1 (rows x columns)
    b = sp.zeros(n2k, k+1)
    for i in range(n2k):
        for j in range(k+1):
            b[i,j] = (xp[i])**j
        # Multiply yp[i] onto the i'th row
        b[i,:] = b[i,:] * yp[i]
    # The first column is the constant, the rest are the coefficient of b
    b = sp.Matrix(b[:,::-1])
    
    # Move the b matrix to the right hand side of the equation except for the firstcolumn
    A = (-b[:,1:]).row_join(A)
    # Delete everything but the first column of b (The constants)
    b = b[:,0]
    
    print(A.shape)

    # Solve the equation system
    result = None
    det = int(A.det())
    gcd, _, _ = extended_euclid_gcd(det, fieldsize)
    if gcd == 1:
        result = pow(det, -1, fieldsize) * A.adjugate() @ b % fieldsize
    else:
        ValueError("Could not find solution")
    # get first k elements of the result i.e. the b coefficents
    print(result)
    bValues = result[:k]
    # The first must always be 1!
    bValues.insert(0,1)
    # Evaluate the error polynomial and find the corrupted shares (they will equal 0)
    errorCollection = []
    for i in range(len(shares)):
        x, r = shares[i]
        result = 0
        bLen = len(bValues)
        for j in range(bLen):
            result += x**(bLen-j-1) * bValues[j]
        result = (result * r) % fieldsize
        errorCollection.append(result == 0)
    # Remove where there are errors
    shares = [share for share, isError in zip(shares,errorCollection) if not isError]
    return shares