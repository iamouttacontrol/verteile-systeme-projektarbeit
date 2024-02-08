import json
import openai
import os
import hashlib
import time
from datetime import datetime
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

#todo: api_key in eine .env Datei packen und sicherer setzen + in gitIgnore packen
#todo: jede nachricht enthält eine eigene JSON? -> macht es Sinn, dass wir in der Antwort die letzten 2-3 Nachrichten mitgeben?
#z.B dass wir einen besserern Kontext geben können? -> was wird die struktur der JSON sein
#remember previous messages sent
#code besser strukturieren


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

save_path = r"C:\Users\tyilm\Desktop\verteile-systeme-projektarbeit\ChatGPT\messages"
messagesPath= r"C:\Users\tyilm\Desktop\verteile-systeme-projektarbeit\ChatGPT\messages\example1.json"


def listenToMessages(chatHistory):
    with open(messagesPath, 'r') as openfile:
        json_object = json.load(openfile)


    message_str = json_object['message'].lower()
    print("Message: "+message_str)  # Zeigt die Alexa-Nachricht an

    # Berechnet die Ähnlichkeit zwischen der Nachricht und "alexa"
    similarity = fuzz.partial_ratio(message_str, "alexa")

    #levienshtein distance -> wie viele Buchstaben müssen wir ändern, um von einem Wort zum anderen zu kommen
    if similarity > 70:
        print("Bot soll antworten")
        return create_chatbot(chatHistory)
    else:
        print("Bot soll nicht antworten")


def create_chatbot(chatHistory):
    messages = chatHistory
    sentiment = checkSentiment(chatHistory)
    #0-1 : 1 ist ein kreativer
    #sentiment=-1 -> ist sehr negativ gelaunt -> eher konsistenterer antworten
    #sentiment=-0 -> ist neutral gelaunt -> eher normale antworten
    #sentiment=1 -> ist sehr positiv gelaunt -> sehr kreative antworten

    min_temp = 0.2
    max_temp = 0.8

    temperature = 0.5 * (sentiment + 1) * (max_temp - min_temp) + min_temp

    print("Temperatur ist: "+str(temperature))
    print("Ich bin ready...!")
    user_input = ""
    chat=[]
    while user_input != "quit":
        user_input = input("Enter your message or 'quit' to exit: ")
        if user_input == "quit":
            break

        messages.append({"role": "user", "content": user_input} )
        messages.append({"role": "system",
                         "content": "Du bist ein Teilnehmer in einem Chatraum. Deine Aufgabe ist es mit anderen Nutzern eine Konversation zu führen. "
                                    "Deine aktuelle Stimmung wird auf einer Skala von -1 (sehr negativ)"
                                    " bis 1 (sehr positiv) bewertet und liegt aktuell bei: "+ str(sentiment)})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,

        )
        #print(response)
        response_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_message})
        print("\n" + response_message + "\n")

        return response_message

def checkSentiment(chatHistory):
    sentiment_value = 0
    for json_object in chatHistory:
        sentiment_value += json_object['sentiment']

    sentiment_value = sentiment_value / len(chatHistory)
    print("Backend: " + str(sentiment_value))
    return sentiment_value
