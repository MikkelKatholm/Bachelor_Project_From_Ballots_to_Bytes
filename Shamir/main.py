import sympy as sp
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
    if type(secrets) is int:
        secrets = [secrets]

    if (n < t):
        raise ValueError("number of shares n must be larger than threshold t")
    k = len(secrets)


    xValues = [i+1 for i in range(-k,t-1)]
    pointsForShares = [ i for i in range(1,n+1) ]
    pointsToIntercect = [random.SystemRandom().randint(0,fieldsize-1) for _ in range(t-1)]
    
    # Make a list of points where (-len(secrets), f(-len(secrets))), (-len(secrets)+1, f(-len(secrets)+1)), ..., (0, f(0)

    values = secrets + pointsToIntercect
    polynomial = list(zip(xValues, values))
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
    secret1 is at x = -numOfSecrets+1
    secret2 is at x = -numOfSecrets+2, 
    .
    .
    .
    secretN is at x = 0
"""
def reconstruct_secrets(shares, numOfSecrets, fieldsize):
    # List of points where the secrets are encoded
    points = [i for i in range(-numOfSecrets+1,1)]

    # Calculate the secrets encoded at the points
    return [ lagrange_interpolate(p, shares, fieldsize) for p in points ]


"""
Berlekamp-Welsh algorithm for error correction 
"""
def berlekamp_welsh(shares, maxNumOfErrors, finalDegree, fieldsize):
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

    # Apply Gaussian elimination modulo p
    A_mod_p = A.applyfunc(lambda x: x % fieldsize)
    b_mod_p = b.applyfunc(lambda x: x % fieldsize)

    # Augment the matrix A_mod_p with the constant vector b_mod_p
    augmented_matrix_mod_p = A_mod_p.row_join(b_mod_p)
    # Reduce the augmented matrix to row-echelon form
    reduced_form_mod_p, _ = augmented_matrix_mod_p.rref()

    # Extract the solution from the reduced form
    solution_mod_p = reduced_form_mod_p[:, -1]

    result = []
    for i in range(len(solution_mod_p)):
        num = solution_mod_p[i].numerator
        den = solution_mod_p[i].denominator
        divm = div_mod(num, den, fieldsize)
        result.append(divm % fieldsize)

    # get first k elements of the result i.e. the b coefficents
    bValues = result[:k]
    # The first must always be 1!
    bValues.insert(0,1)
    # Evaluate the error polynomial and find the corrupted shares (they will equal 0)
    errorCollection = []
    for i in range(n2k):
        x, r = shares[i]
        result = 0
        bLen = len(bValues)
        for j in range(bLen):
            result += x**(bLen-j-1) * bValues[j]
        result = (result * r) % fieldsize
        errorCollection.append(result == 0)

    # Remove where there are errors
    shares = [share for share, isError in zip(shares,errorCollection) if not isError]

    # Sort the shares by x (the first element in the tuple)
    shares.sort(key=lambda x: x[0])

    return shares

"""  
find the polynomial that interpolates the data points and return the coefficients in order of the highest degree to the lowest
f(x)= a**3*x + b**2*x + c*x + d becomes [a,b,c,d]
"""
def get_Poly(dataPoints, threshold, fieldsize):
    x = sp.symbols('x')

    # trim the data points to the threshold
    dataPoints = dataPoints[:(threshold)]

    # Polynomial without a finite field
    poly = sp.polys.polyfuncs.interpolate(dataPoints, x)
    a = (str(poly).replace('- ', '-').replace('+ ', '+').split(' '))[::-1]
    
    for i in range(len(a)):
        if i == 1:
            a[i] = a[i].replace('*x', '')
        else:
            a[i] = a[i].replace("*x**" + str(i),'') 
    a = a[::-1]
    print(a)
    return a

def detect_error(points, threshold, fieldsize):
    def check_Point(dataPoints, checkPoint, fieldsize):
        x = checkPoint[0]
        y = checkPoint[1]
        y_reconstructed = lagrange_interpolate(x, dataPoints, fieldsize)
        return y_reconstructed != y 
    
    if len(points) < threshold:
        raise ValueError("Not enough points to interpolate")

    polyPoints = points[:threshold]
    checkPoints = points[threshold:]

    for point in checkPoints:
        if check_Point(polyPoints, point, fieldsize):
            return True
    return False


def lagrange_For_ElGamal(xPoints, index, threshold, fieldsize):
    result = 1
    for i in range(threshold):
        if i == index:
            continue
        temp = div_mod(xPoints[i], xPoints[i] - xPoints[index], fieldsize)
        result = (result * temp) % fieldsize
    return result
