from twisted.internet import protocol, reactor, endpoints
import json
from pydantic import BaseModel
import websockets
import asyncio

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
        
    async def dataReceived(self, data):
        print(data)
        try:
            received_data = json.loads(data.decode())
            print("received ",received_data)
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
            
class WebSock(protocol.Protocol):   
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
         
    async def server(websocket, path):
        print(f"Client verbunden: {websocket.remote_address}")

        async for message in websocket:
            print(f"Nachricht empfangen von {websocket.remote_address}: {message}")

            # Hier kannst du die empfangenen Nachrichten behandeln und auf sie reagieren

            # Zum Beispiel, um eine Antwort zu senden:
            response = f"Echo: {message}"
            await websocket.send(response)

        print("WebSocket-Server gestartet auf localhost:9000")
    
    
    

class ServerFactory(protocol.ServerFactory):
    def __init__(self):
        self.clients = set()
        
    def buildProtocol(self, addr):
        return WebSock(self)

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:8000").listen(ServerFactory())
    reactor.run()
    