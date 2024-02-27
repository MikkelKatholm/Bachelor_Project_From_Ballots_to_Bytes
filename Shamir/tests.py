from main import *
import sympy.ntheory as nt
import random



""" 
Expected result is generated by https://www.extendedeuclideanalgorithm.com/calculator.php
"""
def test_extended_euclid_gcd():
    inputs = [(10,5), (15, 8), (41, 13), (100, 10), (100, 3), (100, 1), (1203, 123)]
    expected = [(5,0,1), (1,-1,2),(1,-6,19),(10,0,1),(1,1,-33),(1,0,1),(3,9,-88)]
    for i in range(len(inputs)):
        a, b = inputs[i]
        d, x, y = extended_euclid_gcd(a, b)
        assert (d, x, y) == expected[i]



def test_all():
    secret = [1234]
    numOfShares = 6
    threshold = 3
    fieldsize = 1613

    shares = split_secrets(secret, numOfShares, threshold,fieldsize)

    reconstructedSecret1 = reconstruct_secrets(shares[:threshold], 1, fieldsize)
    reconstructedSecret2 = reconstruct_secrets(shares[-threshold:], 1, fieldsize)
    
    assert secret == reconstructedSecret1 == reconstructedSecret2 

def test_with_different_primes():
    # Generate a list of primes
    startingPrime = 1619
    primes = [startingPrime]
    nums = [2**i for i in range(12,100)]
    for i in range(len(nums)):
        workingPrime = nt.nextprime(nums[i] )
        primes.append(workingPrime)

    for i in range(len(primes)):
        workingPrime = primes[i]
        secret = [1234]
        numOfShares = 6
        threshold = 3

        shares = split_secrets(secret, numOfShares, threshold, workingPrime)

        reconstructedSecret1 = reconstruct_secrets(shares[:threshold], 1, workingPrime)
        reconstructedSecret2 = reconstruct_secrets(shares[-threshold:], 1, workingPrime)

        assert secret == reconstructedSecret1 == reconstructedSecret2 


def test_one_lies():
    secret = [1234]
    numOfShares = 6
    threshold = 3
    fieldsize = 1613

    shares = split_secrets(secret, numOfShares, threshold,fieldsize)

    # One share lies 
    shares[0] = (shares[0][0], shares[0][1] - 1)

    reconstructedSecret1 = reconstruct_secrets(shares[:threshold], 1, fieldsize)
    reconstructedSecret2 = reconstruct_secrets(shares[-threshold:], 1, fieldsize)
    assert secret != reconstructedSecret1
    assert secret == reconstructedSecret2

def test_detect_errors():
    secret = [1234]
    numOfShares = 6
    threshold = 3
    fieldsize = 1613

    shares = split_secrets(secret, numOfShares, threshold,fieldsize)

    # One share lies 
    shares[5] = (shares[5][0], shares[5][1] - 1)

    checkPointError = shares[5]
    checkPointHonest = shares[4]
    # First 3 shares (are honest)
    data = shares[:threshold]

    # All shares are honest and the checkpoint is lying
    foundErrors = detect_error(data, checkPointError, fieldsize)

    # All shares are honest and so is the checkpoint
    foundErrors1 = detect_error(data, checkPointHonest, fieldsize)

    assert foundErrors == True
    assert foundErrors1 == False

def additive_test():
    secret1 = [1]
    secret2 = [1]
    secret3 = [0]
    threshold = 2
    numOfShares = 3
    fieldsize = 1613

    #Contruct the shares for each secret
    shares1 = split_secrets(secret1, numOfShares, threshold, fieldsize)
    shares2 = split_secrets(secret2, numOfShares, threshold, fieldsize)
    shares3 = split_secrets(secret3, numOfShares, threshold, fieldsize)

    #Add the shares together
    shares = []
    for i in range(3):
        shares.append((shares1[i][0], (shares1[i][1] + shares2[i][1] + shares3[i][1]) % fieldsize))

    #Reconstruct the secret
    reconstructedSecret = reconstruct_secrets(shares, 1, fieldsize)
    assert reconstructedSecret == [2]

    #Recontruct the secret with only 2 shares from each secret
    reconstructedSecret = reconstruct_secrets(shares[:2], 1, fieldsize)
    assert reconstructedSecret == [2]
    

"""
To reconstruct we must use (numOfSecrets + threshold-1) shares
"""
def test_multiple_secrets():
    secrets = [2,3,4,6,7]
    threshold = 4
    numOfShares = 16
    fieldsize = 1613
    sharedNeeded = len(secrets) + threshold - 1

    shares = split_secrets(secrets, numOfShares, threshold, fieldsize)
    #Reconstruct the secrets
    reconstructedSecret = reconstruct_secrets(shares[:sharedNeeded], len(secrets), fieldsize)
    assert reconstructedSecret == secrets


if __name__ == "__main__":
    test_extended_euclid_gcd()
    test_all()
    test_one_lies()
    test_detect_errors()
    test_with_different_primes()
    additive_test()
    test_multiple_secrets()
    print("Everything passed: 👍")