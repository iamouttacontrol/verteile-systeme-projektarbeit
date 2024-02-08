import json
from twisted.internet import reactor
#from twisted.web.server import Site
#from twisted.web.static import File
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from Translator import translate_and_convert
from ChatGPT import listenToMessages
from Sentiment import sentiment_analysis


class ChatServerProtocol(WebSocketServerProtocol):

    chatHistory = []
    def onConnect(self, request):
        print(f"Client verbunden: {request.peer}")

    def onOpen(self):
        print("WebSocket-Verbindung geöffnet.")
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8')
            print(f"Nachricht empfangen: {message}")
            translated_message = translate_and_convert(json.loads(message))
            print(f"Nachricht übersetzt: {translated_message}")
            sentiment = sentiment_analysis(translated_message)
            sentiment_message = translated_message
            sentiment_message["sentiment"] = sentiment["score"]
            print(f"Nachricht mit Sentiment: {sentiment_message}")
            self.chatHistory.append(sentiment_message)
            print(self.chatHistory)
            if len(self.chatHistory)>5:
                print("History > 5")
                removed_message = self.chatHistory.pop(0)
                print(f"Removed Message {removed_message}")
            else:
                print("History =< 6")
            print(self.chatHistory)
            #self.factory.broadcast(message, self)

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
            print(f"Client {client.peer} registriert.")
            self.clients.remove(client)

    def broadcast(self, message, sender):
        for client in self.clients:
            client.sendMessage(message.encode('utf8'))


if __name__ == "__main__":
    chatServer = ChatServerProtocol()
    #Message 1
    payload = {"name": "Matthias", "message": "Hallo, wie gehts?",
               "language": "EN", "timestamp": 123123, "sentiment": 0}
    payload_encoded = json.dumps(payload).encode('UTF-8')
    chatServer.onMessage(payload_encoded, False)

    #Message 2
    payload = {"name": "Tolga", "message": "Hallo, wie gehts?",
               "language": "EN", "timestamp": 123123, "sentiment": 0}
    payload_encoded = json.dumps(payload).encode('UTF-8')
    chatServer.onMessage(payload_encoded, False)

    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()



