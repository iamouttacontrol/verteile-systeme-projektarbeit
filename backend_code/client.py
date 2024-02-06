from twisted.internet import reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory 
import json

class Client(protocol.Protocol):    
    def __init__(self, lang):
        self.lang = lang
    
    def connectionMade(self):
        data = {"lang":self.lang}
        print("Connected")
        
    def send_data(self):
        self.transport.write(json.dumps("test").encode())        

    def dataReceived(self, data):
        response = json.loads(data.decode())
        print("Response from server:", response)

class ClientFactory(protocol.ReconnectingClientFactory):
    def __init__(self):
        self.lang = "de"
        
    def startedConnecting(self, connector):
        print('Started to connect.')
        
    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        return Client(self.lang)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        

if __name__ == '__main__':
    a = reactor.connectTCP('localhost', 8000, ClientFactory())
    print(type(a))
    reactor.run()
    #a.send_data()
    