import json
import os
from google.cloud import translate_v2 as translate

def translate_text(json):
    credentials_path = "credentials.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =credentials_path
    translate_client = translate.Client()
    message = json["message"]
    print(message)
    target = json["language"]
    print(target)
    if isinstance(message, bytes):
        message = message.decode("utf-8")
    result = translate_client.translate(message, target_language=target)
    print(result)
    return result

with open("tests/test1.json") as test:
    inhalt = json.load(test)

translate_text(inhalt)