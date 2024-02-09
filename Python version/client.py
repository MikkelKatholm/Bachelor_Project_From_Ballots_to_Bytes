import random as rd
#

class Client:
      def __init__(self, vote, numOfServers):
            self.vote = vote
            self.shareOfSecret = []
            self.numOfServers = numOfServers
            self.P = 5081 # Some agreed upon prime number
            self.Z = 5080 # P-1
      

      # Should upgrade to crypto secure random number generator
      def splitSecret(self):
            preliminaryR = 0
            numOfServers = self.numOfServers
            shareOfSecret = self.shareOfSecret
            p = self.P
            for i in range(numOfServers-1):
                  r = rd.randint(0, self.Z)
                  shareOfSecret.append(r)
                  preliminaryR -= r
            r = ((self.vote + preliminaryR) % (p + p) ) % p
            shareOfSecret.append(r)