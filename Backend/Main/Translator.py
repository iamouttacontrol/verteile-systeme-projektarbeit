import os
import html
from google.cloud import translate_v2 as translate

from Backend.Main import Message


def translate_text(message: Message):
    credentials_path = "credentials.json"
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

#def translate_and_convert(message: Message):
#    response = translate_text(message)
#    standard_format = {"name" : message.name, "message" : response["translatedText"], "language" : message.language,
#                       "timestamp" : message.timestamp, "sentiment": message.sentiment}
#    message.message = response["translatedText"]
#    return standard_format

#message = Message(name="Philip", message="Hallo, Ich bin ein Bär", language="EN", timestamp="11:24:39", sentiment=0.0)

#print(type(message))

#print(translate_text(message))
