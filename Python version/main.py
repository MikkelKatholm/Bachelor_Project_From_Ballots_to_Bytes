from client import Client
from server import Server
import copy

numOfServers = 3
numOfClients = 3

def setUp():
    # Create clients and servers
    clients, servers = makeServersAndClients()

    # Each client splits their secret
    splitVote(clients)

    # Each client sends their shares to the servers
    sendShares(clients, servers)
    
    # Each server calculates their S
    serverCalculateS(servers)

    # Each server shares their S with the other servers
    shareS(servers)

    # Each server calculates the vote result
    votes = getAllVotes(servers)

    # Check if the vote result is the same for all servers
    isAllSame = all(x == votes[0] for x in votes)
    msg = "All servers agree on: " + str(votes[0]) if isAllSame else "Servers disagree"
    print(msg)
    
def getAllVotes(servers):
    votes = []
    for server in servers:
        votes.append(server.calculateVoteResult())
    return votes

def makeServersAndClients():
    # Create clients
    clients = []
    for i in range(numOfClients):
        vote = 1 if (i % 2 == 0) else 0 # 1 for even, 0 for odd
        clients.append(Client(vote, numOfServers))

    # Create servers
    servers = []
    for i in range(numOfServers):
        servers.append(Server())
    
    return clients, servers

def splitVote(clients):
    for c in clients:
        c.splitSecret()

def sendShares(clients, servers):
    for i in range(len(clients)):
        clientShares = clients[i].shareOfSecret
        for j in range(len(servers)):
            shareToSend = copy.deepcopy(clientShares)
            shareToSend[j] = 0
            servers[j].receiveShares(shareToSend)


def serverCalculateS(servers):
    for server in servers:
        server.calculateS()

def shareS(servers):
    for i in range(len(servers)):
        for j in range(len(servers)):
            servers[i].receiveS(servers[j].ownS)

setUp()