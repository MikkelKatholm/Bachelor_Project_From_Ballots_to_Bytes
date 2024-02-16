from client import Client
from server import Server
from main import *


def test_2S_1C():
    result, foundErrors = setUp(2,1)
    assert result == 1
    assert foundErrors == False

def test_5S_10C():
    result, foundErrors = setUp(5,10)
    assert result == 5
    assert foundErrors == False

def test_10S_5C():
    result, foundErrors = setUp(10,5)
    assert result == 3
    assert foundErrors == False

def test_10S_10C():
    result, foundErrors = setUp(10,10)
    assert result == 5
    assert foundErrors == False

def test_100S_100C():
    result, foundErrors = setUp(100,100)
    assert result == 50
    assert foundErrors == False


def test_10S_10C_Loop():
    for i in range (1000):
        result, foundErrors = setUp(10,10)
        assert result == 5
        assert foundErrors == False


""" 
Cheating test
    - Simulate a client cheating and sends a different share to a server
    - Client 0 sends r_0_1 to server 2
    - Client 0 sends a different r_0_1 to server 0
    - All servers agree that something went wrong
"""
def test_for_cheating_client():
    servers, clients = makeServersAndClients(3,3)
    # Costumize the setup

    splitVote(clients)

    sendShares(clients, servers)

    # Simulate a client cheats and sends a different share to a server
    servers[0].shareOfSecret[0][1] = (servers[0].shareOfSecret[0][1] + 1) % servers[0].P

    serverCalculateS(servers)

    shareS(servers)

    votes, foundErrors = getAllVotes(servers)

    # Check if the vote result is the same for all servers    

    assert votes[0] == 2
    assert foundErrors == True


""" 
Cheating test
    - Simulate a server cheating and sends a different S to others
    - Server 0 sends A worng S1 to others
    - All servers agree that something went wrong
"""
def test_for_cheating_server():
    servers, clients = makeServersAndClients(5,4)
    # Costumize the setup

    splitVote(clients)

    sendShares(clients, servers)

    serverCalculateS(servers)

    # Simulate a server cheats and sends a different S to others
    servers[0].ownS[1] = (servers[0].ownS[1] + 1) % servers[0].P

    shareS(servers)

    votes, foundErrors = getAllVotes(servers)

    # Check if the vote result is the same for all servers
    
    assert votes[0] == 2
    assert foundErrors == True


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

    shareS(servers)

    votes, foundErrors = getAllVotes(servers)

    # Check if the vote result is the same for all servers
    

    assert votes[0] == 3
    assert foundErrors == True



if __name__ == "__main__":
    test_2S_1C()
    test_5S_10C()
    test_10S_5C()
    test_10S_10C()
    test_10S_10C_Loop()
    test_100S_100C()
    test_for_cheating_client()
    test_for_cheating_server()
    test_error_correction_should_work()
    print("Everything passed: 👍")