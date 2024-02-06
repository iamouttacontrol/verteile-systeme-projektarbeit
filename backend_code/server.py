from twisted.internet import protocol, reactor, endpoints
import json

class Server(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        
    def connectionMade(self):
        self.factory.clients.add(self)
        
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        
    def dataReceived(self, data):
        received_data = json.loads(data.decode())

        print(received_data)

        response_data = {"response": "Received data successfully"}
        
        for c in self.factory.clients:
            c.transport.write(json.dumps(response_data).encode())

class ServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()
        
    def buildProtocol(self, addr):
        return Server(self)

if __name__ == '__main__':
    # Server starten
    endpoints.serverFromString(reactor, "tcp:8000").listen(ServerFactory())
    reactor.run()