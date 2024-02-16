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


""" 
Cheating test
    - Simulate a client cheating and sends a different share to a server
    - Client 0 sends r_0_1 to server 2
    - Client 0 sends a different r_0_1 to server 0
    - All servers agree that something went wrong
"""
def test_for_chearing_client():
    servers, clients = makeServersAndClients(3,3)
    # Costumize the setup

    splitVote(clients)

    sendShares(clients, servers)

    # Simulate a client cheats and sends a different share to a server
    servers[0].shareOfSecret[0][1] = (servers[0].shareOfSecret[0][1] + 1) % servers[0].P

    serverCalculateS(servers)

    shareS(servers)

    votes = getAllVotes(servers)

    # Check if the vote result is the same for all servers    
    isAllGood = True if votes[0] != -1 else False

    msg = "All servers agree on: " + str(votes[0]) if isAllGood else "Something went wrong"
    assert msg == "Something went wrong"
    assert isAllGood == False



""" 
Cheating test
    - Simulate a server cheating and sends a different S to others
    - Server 0 sends A worng S1 to others
    - All servers agree that something went wrong
"""
def test_for_cheating_server():
    servers, clients = makeServersAndClients(3,3)
    # Costumize the setup

    splitVote(clients)

    sendShares(clients, servers)

    serverCalculateS(servers)

    # Simulate a server cheats and sends a different S to others
    servers[0].ownS[1] = (servers[0].ownS[1] + 1) % servers[0].P

    shareS(servers)

    votes = getAllVotes(servers)

    # Check if the vote result is the same for all servers
    
    isAllGood = True if votes[0] != -1 else False

    msg = "All servers agree on: " + str(votes[0]) if isAllGood else "Something went wrong"
    assert msg == "Something went wrong"
    assert isAllGood == False


""" 
Error correction test
    - 10 server
    - 3 corupted servers
    - 5 clients
"""
def test_error_correction_should_work():
    servers, clients = makeServersAndClients(10,5)
    # Costumize the setup
    p = servers[0].P

    splitVote(clients)

    sendShares(clients, servers)

    serverCalculateS(servers)

    # Simulate a server cheats and sends a different S to others
    servers[0].ownS[1] = (servers[0].ownS[1] + 1) % p
    servers[1].ownS[2] = (servers[1].ownS[2] + 1) % p
    servers[2].ownS[3] = (servers[2].ownS[3] + 1) % p

    for i in range(10):
        print(servers[i].ownS)
    

    shareS(servers)

    votes = getAllVotes(servers)

    # Check if the vote result is the same for all servers
    
    isAllGood = True if votes[0] != -1 else False

    msg = "All servers agree on: " + str(votes[0]) if isAllGood else "Something went wrong"
    assert msg == "All servers agree on: 3"
    assert isAllGood == True



if __name__ == "__main__":
    test_2S_1C()
    test_5S_10C()
    test_10S_5C()
    test_10S_10C()
    test_10S_10C_Loop()
    test_100S_100C()
    test_for_chearing_client()
    test_for_cheating_server()
    #test_error_correction_should_work()
    print("Everything passed: 👍")