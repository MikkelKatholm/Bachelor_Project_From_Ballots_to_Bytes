from client import Client
from server import Server
from main import *

""" 
Tests covered:
    - More servers than clients
    - More clients than servers
    - Equal amount of servers and clients
    - Minimum amount of servers and clients (2,1)
"""




def test_2S_1C():
    result, allAgree = setUp(2,1)
    assert result == 1
    assert allAgree == True

def test_5S_10C():
    result, allAgree = setUp(5,10)
    assert result == 5
    assert allAgree == True

def test_10S_5C():
    result, allAgree = setUp(10,5)
    assert result == 3
    assert allAgree == True

def test_10S_10C():
    result, allAgree = setUp(10,10)
    assert result == 5
    assert allAgree == True

def test_100S_100C():
    result, allAgree = setUp(100,100)
    assert result == 50
    assert allAgree == True


def test_10S_10C_Loop():
    for i in range (1000):
        result, allAgree = setUp(10,10)
        assert result == 5
        assert allAgree == True

def test_For_Cheaters():
    clients, servers = makeServersAndClients(3,3)
    # Costumize the setup

    clients[0].shareOfSecret = [2920,2006,156]
    clients[1].shareOfSecret = [4372,3631,2159]
    clients[2].shareOfSecret = [2786,1724,572]

    sendShares(clients, servers)

    # Simulate a client cheats and sends a different share to a server
    servers[0].shareOfSecret[0][1] = 3000

    serverCalculateS(servers)
    shareS(servers)
    votes = getAllVotes(servers)

    # Check if the vote result is the same for all servers
    
    isAllGood = True if votes[0] != -1 else False

    msg = "All servers agree on: " + str(votes[0]) if isAllGood else "Something went wrong"
    assert msg == "Something went wrong"
    assert isAllGood == False




if __name__ == "__main__":
    test_2S_1C()
    test_5S_10C()
    test_10S_5C()
    test_10S_10C()
    test_10S_10C_Loop()
    test_100S_100C()
    test_For_Cheaters()
    print("Everything passed: 👍")