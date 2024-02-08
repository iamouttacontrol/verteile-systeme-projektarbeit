import json
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from Message import MessageFromClient, MessageToClient
from Translator import translate_text
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
            message = json.loads(message)
            # message = MessageFromClient.model_validate(message["username"], message["message"], message["language"], message["timestamp"])
            message = MessageFromClient.model_validate(message)

            if message.language != "EN":
                message.language = "EN"

            # print(f"Nachricht empfangen: {message}")
            message = translate_text(message)
            # print(f"Nachricht übersetzt: {message}")
            message = sentiment_analysis(message)
            # print(f"Nachricht mit Sentiment: {message}")
            self.chatHistory.append(message)
            # print(self.chatHistory)
            # print(self.chatHistory[len(self.chatHistory)-1])
            if len(self.chatHistory) > 5:
                # print("History > 5")
                removed_message = self.chatHistory.pop(0)
                # print(f"Removed Message {removed_message}")
            else:
                # print("History =< 6")
                pass

            listenToMessages(self.chatHistory)

            # self.factory.broadcast(message, self)

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
            message.language = client.language
            message = translate_text(message)
            client.sendMessage(message)


if __name__ == "__main__":
    chatServer = ChatServerProtocol()

    '''
    Message = b'{"username":"test","message":"alexa, mir gehts nicht gut","timestamp":"14:42:21","language":"de"}'
    chatServer.onMessage(Message, False)
    '''
    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()
