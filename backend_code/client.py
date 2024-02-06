from twisted.internet import reactor, protocol
import json

class Client(protocol.Protocol):
    def connectionMade(self):
        data = {"message": "Hello, server!"}
        self.transport.write(json.dumps(data).encode())

    def dataReceived(self, data):
        response = json.loads(data.decode())
        print("Response from server:", response)

class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason)
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason)
        reactor.stop()

if __name__ == '__main__':
    reactor.connectTCP('localhost', 8000, ClientFactory())
    reactor.run()