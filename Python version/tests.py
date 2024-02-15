from client import Client
from server import Server
from main import setUp

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


if __name__ == "__main__":
    test_2S_1C()
    test_5S_10C()
    test_10S_5C()
    test_10S_10C()
    test_100S_100C()
    print("Everything passed: 👍")