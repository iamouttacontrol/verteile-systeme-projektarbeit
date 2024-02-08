import os
import html
from google.cloud import translate_v2 as translate

from Backend.Main import MessageFromClient, MessageToClient


def translate_text(message: MessageFromClient | MessageToClient):
    credentials_path = "C:/Users/Matthias Wohlmacher/PycharmProjects/verteile-systeme-projektarbeit/Backend/Main/credentials.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    translate_client = translate.Client()
    message_str = message.message
    target = message.language
    if isinstance(message_str, bytes):
        message_str = message_str.decode("utf-8")
    result = translate_client.translate(message_str, target_language=target)
    result["translatedText"] = html.unescape(result["translatedText"])
    message.message = result["translatedText"]
    return message

message = MessageToClient(username="Philip", message="Hallo, Ich bin ein Bär", language="EN",
                          timestamp="11:24:39", sentiment=0.0)

print(type(message))
print(translate_text(message))
