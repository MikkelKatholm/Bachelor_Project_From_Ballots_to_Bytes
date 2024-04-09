import sys
sys.path.append("../")
import random
import key_gen
from main import *
import unittest
import Shamir.main as shamir



# For all tests we use a 128 bit prime number unless otherwise specified in the test
bits = 128

class TestExample1(unittest.TestCase):

    def test_singleSecretTest(self):
        p, g, pk, sk = gen_keys(bits)
        m = 0 # Message to encrypt
        c = encrypt(pk,m,p,g)
        d = decrypt(sk,g,c,p,1)

        isSame = d == m
        self.assertTrue(isSame, "Decryption failed")


    def test_additiveTest(self):
        p, g, pk, sk = gen_keys(bits)
        m1 = 0 # Message to encrypt
        m2 = 1 # Message to encrypt
        (c11, c12) = encrypt(pk,m1,p,g)
        (c21, c22) = encrypt(pk,m2,p,g)
        
        c = (c11*c21, c12*c22)

        d = decrypt(sk,g,c,p,2)
        isSame = d == (m1+m2)
        self.assertTrue(isSame, "Decryption failed")

    
    def test_multiplicativeTest(self):
        p, g, pk, sk = gen_keys(bits)
        c1, c2 = 1,1
        totalVote = 0
        voters = 100
        for _ in range(voters):
            m = random.SystemRandom().randint(0,1)
            totalVote += m
            c = encrypt(pk,m,p,g)
            c1 *= c[0]
            c2 *= c[1]
        c = (c1,c2)

        print(f"totalVote: {totalVote}")
        result = decrypt(sk,g,c,p, voters)

        isSame = result == totalVote
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
    print("Test ran: ", result.testsRun)
    print("Errors: ", len(result.errors))
    print("Failures: ", len(result.failures))
    print("Skipped: ", len(result.skipped))
    print("Success: ", result.wasSuccessful())
    print("\n")

