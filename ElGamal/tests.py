import sys
sys.path.append("../")
import random

from main import *
import unittest
import Shamir.main as shamir
import time



# For all tests we use a 128 bit prime number unless otherwise specified in the test
bits = 128

class TestExample1(unittest.TestCase):

    def test_singleSecretTest(self):
        pk, sk = gen_keys(bits)
        m = 0 # Message to encrypt
        c = encrypt(pk, m)
        d = decrypt_for_additive(sk,c,1)

        isSame = d == m
        self.assertTrue(isSame, "Decryption failed")


    def test_additiveTest(self):
        pk, sk = gen_keys(bits)
        m1 = 0 # Message to encrypt
        m2 = 1 # Message to encrypt
        (c11, c12) = encrypt(pk, m1)
        (c21, c22) = encrypt(pk, m2)
        
        c = (c11*c21, c12*c22)

        d = decrypt_for_additive(sk,c,2)
        isSame = d == (m1+m2)
        self.assertTrue(isSame, "Decryption failed")

    
    def test_multiplicativeTest(self):
        pk, sk = gen_keys(bits)
        c1, c2 = 1,1
        totalVote = 0
        voters = 100
        for _ in range(voters):
            m = random.SystemRandom().randint(0,1)
            totalVote += m
            c = encrypt(pk, m)
            c1 *= c[0]
            c2 *= c[1]
        c = (c1,c2)

        result = decrypt_for_additive(sk, c, voters)

        isSame = result == totalVote
        self.assertTrue(isSame, "Decryption failed")
 

    def test_ElGamal_With_Shamir_Key(self):
        bits = 12
        pk, sk = gen_keys(bits)
        m = 0
        keyHolders = 3
        threshold = 2
        shares = generate_key_shares(sk, keyHolders, threshold)

        c = encrypt(pk, m)
        c1, _ = c
        dis = [(share[0], calculate_di_for_shamir(c1, share)) for share in shares]   # Correct, tested by hand
        result = decrypt_for_shamir(dis, c, threshold, 1)

        isSame = result == m
        self.assertTrue(isSame, "Decryption failed")

    def test_ElGamal_Shamir_Multiple_Voters(self):
        startTime = time.time()
        pk, sk = gen_keys(bits)
        c1, c2 = 1,1
        totalVote = 0
        voters = 3_000
        keyHolders = 30
        threshold = 20
        shares = generate_key_shares(sk, keyHolders, threshold)

        for _ in range(voters):
            m = random.SystemRandom().randint(0,1)
            totalVote += m
            c = encrypt(pk, m)
            c1 *= c[0]
            c2 *= c[1]
        c = (c1,c2)
        dis = [(share[0], calculate_di_for_shamir(c1, share)) for share in shares]
        result = decrypt_for_shamir(dis, c, threshold, voters)
        isSame = result == totalVote
        endTime = time.time()
        print(f"Time taken for {voters} voters: {round(endTime-startTime,4)} seconds")
        self.assertTrue(isSame, "Decryption failed")



def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestExample1))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())

    # Format the "ok" messages in a straight line
    print("\n")
    print("Test ran: \t ", result.testsRun)
    print("Errors: \t ", len(result.errors))
    print("Failures: \t ", len(result.failures))
    print("Skipped: \t ", len(result.skipped))
    print("Success: \t ", result.wasSuccessful())
    print("\n")
