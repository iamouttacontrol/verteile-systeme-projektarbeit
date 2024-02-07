from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

class ChatServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print(f"Client verbunden: {request.peer}")

    def onOpen(self):
        print("WebSocket-Verbindung geöffnet.")
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8')
            print(f"Nachricht empfangen: {message}")
            self.factory.broadcast(message, self)

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket-Verbindung geschlossen: {reason}")
        self.factory.unregister(self)

class ChatServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        super().__init__(url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print(f"Client {client.peer} deregistriert.")
            self.clients.remove(client)

    def broadcast(self, message, sender):
        for client in self.clients:
            client.sendMessage(message.encode('utf8'))

if __name__ == "__main__":
    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()
