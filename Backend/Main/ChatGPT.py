import json
from datetime import datetime

import openai
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

from Message import MessageToClient

#todo: api_key in eine .env Datei packen und sicherer setzen + in gitIgnore packen
#todo: jede nachricht enthält eine eigene JSON? -> macht es Sinn, dass wir in der Antwort die letzten 2-3 Nachrichten mitgeben?
#z.B dass wir einen besserern Kontext geben können? -> was wird die struktur der JSON sein
#remember previous messages sent
#code besser strukturieren


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def listenToMessages(chatHistory):
    message = chatHistory[len(chatHistory)-1]

    message_str = message.message
    print("Message: "+message_str)  # Zeigt die Alexa-Nachricht an

    # Berechnet die Ähnlichkeit zwischen der Nachricht und "alexa"
    similarity = fuzz.partial_ratio(message_str, "alexa")

    #levienshtein distance -> wie viele Buchstaben müssen wir ändern, um von einem Wort zum anderen zu kommen
    if similarity > 70:
        print("Bot soll antworten")
        return create_chatbot(chatHistory)
    else:
        print("Bot soll nicht antworten")
        return None


def create_chatbot(chatHistory):
    messages = []
    sentiment = checkSentiment(chatHistory)
    #0-1 : 1 ist ein kreativer
    #sentiment=-1 -> ist sehr negativ gelaunt -> eher konsistenterer antworten
    #sentiment=-0 -> ist neutral gelaunt -> eher normale antworten
    #sentiment=1 -> ist sehr positiv gelaunt -> sehr kreative antworten

    min_temp = 0.2
    max_temp = 0.8
    # auszug aus der doku
    # Higher values like 0.8 will make the output more random, while lower values like 0.2
    # will make it more focused and deterministic.
    temperature = 0.5 * (sentiment + 1) * (max_temp - min_temp) + min_temp

    print("temperature for bot is: " + str(temperature))

    for message in chatHistory:
        messages.append({"role": "user", "content": f"{message.message}"})


    messages.append({"role": "system",
                    "content": "Du bist ein intelligenter Assistent in einem Chatraum."
                                " Deine Aufgabe ist es, mit relevanten und hilfreichen Antworten"
                                " zu reagieren. Zusätzlich hast du Zugriff auf die letzten bis zu 5 Nachrichten aus"
                                " dem Chatverlauf. Diese Nachrichten enthalten jeweils den Nickname des Teilnehmers"
                                " und die Nachricht selbst. Deine Antworten sollten sowohl den Kontext dieser "
                                "Nachrichten berücksichtigen. Deine Stimmung wird algorithmisch auf einer Skala von -1 "
                                "(sehr negativ) bis 1 (sehr positiv) erfasst und soll in deinen Antworten"
                                " widergespiegelt werden. Deine aktuelle Stimmung liegt bei: "+ str(sentiment)
                     }

    )
    response = openai.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        temperature=temperature,
        max_tokens=1000,
        frequency_penalty=0,
        presence_penalty=0,
    )
    #print(response)
    response_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_message})
    print("\n" + response_message + "\n")

    date_time = datetime.now()
    str_date_time = date_time.strftime("%H:%M:%S")
    return MessageToClient(username="Alexa", message=response_message, language="EN", timestamp=str_date_time, sentiment=sentiment)

def checkSentiment(chatHistory):
    sentiment_value = 0
    for message in chatHistory:
        sentiment_value += message.sentiment

    sentiment_value = sentiment_value / len(chatHistory)
    return sentiment_value
