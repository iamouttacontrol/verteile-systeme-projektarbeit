import json
import openai
import os
import hashlib
import time
from datetime import datetime

#todo: api_key in eine .env Datei packen und sicherer setzen + in gitIgnore packen
#todo: jede nachricht enthält eine eigene JSON? -> macht es Sinn, dass wir in der Antwort die letzten 2-3 Nachrichten mitgeben?
#z.B dass wir einen besserern Kontext geben können? -> was wird die struktur der JSON sein
#todo welche Sprachen sollten wir nehmen? deutsch, englisch, spanisch?
#laut openAI gibt es Paramater Temperature=Genauigkeit der Informationen, Max_tokens= wie lang ist die Antwort
#todo: schau dir ChatCompletion vs. Completions an -> was ist der Unterschied?
#todo: Was ist default, was ist Streaming? -> was ist der Unterschied?

api_key = os.getenv('OPENAI_API_KEY', 'key') #paste key
openai.api_key = api_key


save_path = r"C:\Users\tyilm\Desktop\verteile-systeme-projektarbeit\ChatGPT\messages"

def listenToMessges():
    with open('messages/example2.json', 'r') as openfile:
        json_object = json.load(openfile)

    message_str = json_object['message'].lower()
    if "alexa" not in message_str:
        print("Bot soll nicht antworten")
        return
    else: create_chatbot()

    print(message_str)  # Zeigt die Alexa-Nachricht an


def create_chatbot():
    messages = []
    system_msg = input("Hallo mein Name ist Alexa. Was soll mein Stil sein?\n")
    messages.append({"role": "system", "content": system_msg})

    print("Ich bin ready...!")
    user_input = ""
    while user_input != "quit":
        user_input = input("Enter your message or 'quit' to exit: ")
        if user_input == "quit":
            break

        messages.append({"role": "user", "content": user_input})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_message})
        print("\n" + response_message + "\n")

        save_response_as_json(response_message)


def save_response_as_json(message):
    # Erstellen eines Hash-Codes basierend auf der aktuellen Zeit -> damitt wir immer ein indiduellen namen haben
    hash_code = hashlib.sha256(str(time.time()).encode()).hexdigest()[:10]
    file_name = f"message-{hash_code}.json"
    full_path = os.path.join(save_path, file_name)
    current_time = datetime.now().strftime("%H:%M:%S")


    # Erstellen der Nachrichtenstruktur
    message_structure = {
        "nickname": "ChatGPT",
        "message": message,
        "time": current_time,
        "language": "de"
    }

    # Sicherstellen, dass der Speicherpfad existiert
    os.makedirs(save_path, exist_ok=True)

    # Speichern der Nachricht in einer JSON-Datei im angegebenen Verzeichnis
    # Öffnen der Datei mit UTF-8 Kodierung
    with open(full_path, 'w', encoding='utf-8') as outfile:
        # Sicherstellen, dass Umlaute und spezielle Zeichen korrekt gespeichert werden
        json.dump(message_structure, outfile, ensure_ascii=False, indent=4)

    print(f"Nachricht gespeichert in: {full_path}")



listenToMessges()
