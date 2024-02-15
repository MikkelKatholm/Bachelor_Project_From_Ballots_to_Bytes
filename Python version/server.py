
class Server:
    def __init__(self):
        self.P = 5081 # Some agreed upon prime number
        self.Z = 5080
        self.shareOfSecret = []
        self.S = []
        self.ownS = []

    def receiveShares(self, share):
        self.shareOfSecret.append(share)

    def calculateS(self):
        S = []
        for i in range(len(self.shareOfSecret[0])):
            sum = 0
            for j in range(len(self.shareOfSecret)):
                sum += self.shareOfSecret[j][i]
            S.append(sum % self.P)
        self.ownS = S
    
    def receiveS(self, S):
        self.S.append(S)
            
    def calculateVoteResult(self):
        S = [0 for i in range(len(self.ownS))]
        for i in range(len(self.ownS)):
            for j in range(len(self.S)):
                S[i] = max(S[i], self.S[j][i])
        return sum(S) % self.P