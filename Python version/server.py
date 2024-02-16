
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


    def checkAllSAreSame(self):
        # Check if all S_i are the same for all servers, ignore when S_i is 0
        check = True
        for i in range(len(self.S)):
            checkArray = []
            for j in range(len(self.S[i])):
                if i != j:
                    checkArray.append(self.S[j][i])
            #Check if all elements in checkArray are the same
            self.ownS[i] = max(set(checkArray), key = checkArray.count)
            if not all(x == checkArray[0] for x in checkArray):
                check = False
        return check


    def correct_errors(self):
        for i in range(len(self.S)):
            checkArray = []
            for j in range(len(self.S[i])):
                if i != j:
                    checkArray.append(self.S[j][i])
            # Find majority
            majority = max(set(checkArray), key = checkArray.count)
            self.ownS[i] = majority


    """ 
    Cheks if all S_i are the same for all servers
    If not, correct the errors
    Returns the vote result and a boolean indicating if errors were found 
    """
    def calculateVoteResult(self):
        isAllGood = self.checkAllSAreSame()
        foundErrors = False
        if not isAllGood:
            self.correct_errors()
            foundErrors = True
        s = sum(self.ownS)
        return s % self.P, foundErrors
