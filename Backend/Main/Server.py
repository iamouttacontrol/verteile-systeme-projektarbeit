import json
import traceback
from twisted.internet import reactor, task
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.websocket.types import ConnectionDeny
from Message import MessageFromClient, MessageToClient
from http import HTTPStatus
from pydantic import BaseModel
#from Translator import translate_text
#from ChatGPT import listenToMessages
#from Sentiment import sentiment_analysis


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
            print("empty message ", payload, " empty rest")
            print(type(payload))
            if not isBinary:
                message = payload.decode('utf8')
                print(type(message))
                print(f"Nachricht empfangen: {message}")
                message = json.loads(message)
                # message = MessageFromClient.model_validate(message["username"], message["message"], message["language"], message["timestamp"])
                message = MessageFromClient.model_validate(message)
                
                if (self.language is None):
                    self.language = message.language
                    print("set user language to", self.language)
                    
                if (self.username is None):
                    self.username = message.username
                    print("linked user with username", self.username)
                    
        

                if message.language != "en":
                    message.language = "en"
                   
                ''' 
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
                '''
                self.factory.broadcast(message, self)

                '''
                chat_response = listenToMessages(self.chatHistory)
                if chat_response != message:
                    self.factory.broadcast(chat_response, self)
                '''
   
        except Exception:
            print(traceback.format_exc())
            #raise ConnectionDeny(400, "wrong parameter in request")
            raise HTTPStatus(status=400, reason="wrong parameter in request")
        

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket-Verbindung geschlossen: {reason}")
        self.factory.unregister(self)


class ChatServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        super().__init__(url)
        self.clients = [] 
        self.loop = task.LoopingCall(self.sendCurrentUsers)   
        
    def getUsernameAndLang(self):
        client_list = []
        for client in self.clients:
            client_list.append({"username":client.username, "language":client.language})
        return client_list
        
    def sendCurrentUsers(self):
        number_of_clients = len(self.clients)
        client_list = self.getUsernameAndLang()
        print(client_list)
        for client in self.clients:
            try: 
                if not (client.username is None or client.language is None):
                    message = json.dumps({"clientsOnline":client_list, "numOfClients":number_of_clients})
                    client.sendMessage(message.encode('utf-8'))
            except:
                pass
        
    def register(self, client):
        if client not in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.append(client)
        if len(self.clients) > 0:
            self.loop.start(5)

    def unregister(self, client):
        if client in self.clients:
            print(f"Client {client.peer} registriert.")
            self.clients.remove(client)
        if len(self.clients) < 1:
            self.loop.stop()

    def broadcast(self, message, sender):
        print(sender)
        for client in self.clients:
            message.language = client.language
            print(message)
            print(type(message.language))
            client.sendMessage(json.dumps(message.__dict__).encode('utf-8'))
            

if __name__ == "__main__":
    '''
    chatServer = ChatServerProtocol()
    
    Message = b'{"username":"test","message":"alexa, mir gehts nicht gut","timestamp":"14:42:21","language":"de"}'
    chatServer.onMessage(Message, False)
    '''
    
    #connect_message = b'{"language":"de"}'
    
    #chatServer.onConnect(c)
    factory = ChatServerFactory("ws://localhost:9000")
    factory.protocol = ChatServerProtocol
    reactor.listenTCP(9000, factory)
    print("WebSocket-Server gestartet auf Port 9000.")
    reactor.run()
