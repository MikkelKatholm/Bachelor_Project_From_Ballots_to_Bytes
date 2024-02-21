from main import *
import sympy.ntheory as nt
import random



""" 
Expected result is generated by https://www.extendedeuclideanalgorithm.com/calculator.php
"""
def test_extended_euclid_gcd_should_return_correct_result():
    inputs = [(10,5), (15, 8), (41, 13), (100, 10), (100, 3), (100, 1), (1203, 123)]
    expected = [(5,0,1), (1,-1,2),(1,-6,19),(10,0,1),(1,1,-33),(1,0,1),(3,9,-88)]
    for i in range(len(inputs)):
        a, b = inputs[i]
        d, x, y = extended_euclid_gcd(a, b)
        assert (d, x, y) == expected[i]

""" 
Expected results from example on wikipedia: https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing
"""
def test_split_secret():
    secret = 1234
    num = 6
    threshold = 3
    fieldsize = 1613
    excepted = [(1,1494),(2,329),(3,965),(4,176),(5,1188),(6,775)]
    if (num < threshold):
        raise ValueError("Threshold t must be larger than number of shares n")
    # Make polynomial of degree t-1, where f(0) = secret
    coefficients = [secret] + [166, 94]
    points = []
    for i in range(1, num+1):
        value = polynomialValueAtX(coefficients, i,fieldsize)
        value %= 1613
        points.append((i, value))
    
    assert points == excepted


""" 
Tests that polynomialValueAtX with poly = 
"""
def test_polynomialValueAtX():
    fieldsize = 1613
    # Correct code stolen from Wikipedia
    def polyAtX(poly, x, prime):
        accum = 0
        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= prime
        return accum

    for x in range(10):
        poly = [random.randint(0, fieldsize-1) for _ in range(10)]
        value = polynomialValueAtX(poly, x, fieldsize)
        assert value == polyAtX(poly,x , fieldsize)


def test_All():
    secret = 1234
    numOfShares = 6
    threshold = 3
    fieldsize = 1613

    shares = split_secret(secret, numOfShares, threshold,fieldsize)

    reconstructedSecret1 = reconstructSecret(shares[:threshold], threshold,fieldsize)
    reconstructedSecret2 = reconstructSecret(shares[-threshold:], threshold,fieldsize)

    assert secret == reconstructedSecret1 == reconstructedSecret2 

def test_all_with_different_primes():

    # Generate a list of primes
    startingPrime = 1619
    primes = [startingPrime]
    nums = [2**i for i in range(12,100)]
    for i in range(len(nums)):
        workingPrime = nt.nextprime(nums[i] )
        primes.append(workingPrime)

    for i in range(len(primes)):
        workingPrime = primes[i]
        secret = 1234
        numOfShares = 6
        threshold = 3

        shares = split_secret(secret, numOfShares, threshold, workingPrime)

        reconstructedSecret1 = reconstructSecret(shares[:threshold], threshold, workingPrime)
        reconstructedSecret2 = reconstructSecret(shares[-threshold:], threshold, workingPrime)

        assert secret == reconstructedSecret1 == reconstructedSecret2 


def test_One_Lies():
    secret = 1234
    numOfShares = 6
    threshold = 3
    fieldsize = 1613

    shares = split_secret(secret, numOfShares, threshold,fieldsize)

    shares[0] = (shares[0][0], shares[0][1] - 1)

    reconstructedSecret1 = reconstructSecret(shares[:threshold], threshold,fieldsize)
    reconstructedSecret2 = reconstructSecret(shares[-threshold:], threshold,fieldsize)

    assert secret != reconstructedSecret1
    assert secret == reconstructedSecret2

if __name__ == "__main__":
    test_extended_euclid_gcd_should_return_correct_result()
    test_split_secret()
    test_polynomialValueAtX()
    test_All()
    test_One_Lies()
    test_all_with_different_primes()
    print("Everything passed: 👍")