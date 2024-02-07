from twisted.internet import protocol, reactor, endpoints
import json
from pydantic import BaseModel

class Json(BaseModel):
    name: str
    message: str
    language: str
    timestamp: int | None = None

class Server(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        print("SERVER CREATED")
        
    def connectionMade(self):
        self.factory.clients.add(self)
        print("Client connected:", self.transport.getPeer())
        print(len(self.factory.clients))
        self.lang = "en"
        
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        
    def dataReceived(self, data: Json):
        received_data = json.loads(data.decode())

        print("received ",received_data)
        try:
            language = received_data["lang"]
            print("changed language to:" + language)
            self.lang = received_data["lang"]
        except:    
            try:
                for c in self.factory.clients:
                    #print(received_data)
                    #print(received_data["message"])
                    response_data = {"response": received_data}
                    c.transport.write(json.dumps(response_data).encode())
            except:
                pass

class ServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()
        
    def buildProtocol(self, addr):
        return Server(self)

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:8000").listen(ServerFactory())
    reactor.run()
    