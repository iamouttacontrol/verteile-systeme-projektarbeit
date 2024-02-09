import json
import traceback
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from Message import MessageFromClient, MessageToClient
from http import HTTPStatus
from Translator import translate_text
from ChatGPT import listenToMessages
from Sentiment import sentiment_analysis


class ChatServerProtocol(WebSocketServerProtocol):
    chatHistory = []

    def onConnect(self, request):
        self.language = None
        self.username = None
        print(f"Client verbunden: {request.peer}")

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        try:
            if not isBinary:
                try:
                    message = payload.decode("utf8")
                    message = json.loads(message)
                    print(f"message received: {message}")
                    message = MessageFromClient.model_validate(message)
                    message_copy = MessageFromClient.model_validate(message.__dict__)

                    if self.language is None or self.username is None:
                        self.language = message.language
                        self.username = message.username
                        print("set user language to", self.language)
                        print("linked user with username", self.username)
                        self.factory.sendCurrentUsers()

                    if message_copy.language != "en":
                        message_copy.language = "en"

                    message_copy = translate_text(message_copy)
                    print(
                        f"translated message for sentiment to: {message_copy.message}"
                    )
                    message_copy = sentiment_analysis(message_copy)
                    print(f"sentiment generated: {message_copy.sentiment}")

                    message = MessageToClient(
                        username=message.username,
                        message=message.message,
                        language=message.language,
                        timestamp=message.timestamp,
                        sentiment=message_copy.sentiment,
                    )
                    self.chatHistory.append(message)
                    print(f"Message '{message.message}' added to chat history")

                    while len(self.chatHistory) > 5:
                        message_old = self.chatHistory.pop(0)
                        print(
                            f"old message '{message_old.message} removed from chat history"
                        )

                    self.factory.broadcast(message, self)
                    print(f"Message '{message.message}' broadcasted")

                    chat_response = listenToMessages(self.chatHistory)
                    print(chat_response)
                    if chat_response is not None:
                        self.chatHistory.append(chat_response)
                        print(
                            f"Message '{chat_response.message}' added to chat history"
                        )
                        self.factory.broadcast(chat_response, self)
                        print(f"Message '{chat_response.message}' broadcasted")

                        while len(self.chatHistory) > 5:
                            message_old = self.chatHistory.pop(0)
                            print(
                                f"old message '{message_old.message} removed from chat history"
                            )
                except:
                    print(traceback.format_exc())

        except Exception:
            print(traceback.format_exc())
            raise HTTPStatus(status=400, reason="wrong parameter in request")

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket-Verbindung geschlossen: {reason}")
        self.factory.unregister(self)


class ChatServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        super().__init__(url)
        self.clients = []

    def getUsernameAndLang(self):
        client_list = []
        for client in self.clients:
            if not (client.username is None or client.language is None):
                client_list.append(
                    {"username": client.username, "language": client.language}
                )
        return client_list

    def sendCurrentUsers(self):
        number_of_clients = len(self.clients)
        client_list = self.getUsernameAndLang()
        print(client_list)
        for client in self.clients:
            try:
                if not (client.username is None or client.language is None):
                    message = json.dumps(
                        {
                            "clientsOnline": client_list,
                            "numOfClients": number_of_clients,
                        }
                    )
                    client.sendMessage(message.encode("utf-8"))
            except:
                print(traceback.format_exc())

    def register(self, client):
        if client not in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.remove(client)
        if len(self.clients):
            self.sendCurrentUsers()

    def broadcast(self, message, sender):
        print(sender)
        for client in self.clients:
            if message.language != client.language:
                message.language = client.language
                message = translate_text(message)
                print(f"Message translated for {client.username}")
            client.sendMessage(json.dumps(message.__dict__).encode("utf-8"))


if __name__ == "__main__":
    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()
