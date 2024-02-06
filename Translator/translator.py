import json
import os
from google.cloud import translate_v2 as translate
import html

def translate_text(json):
    credentials_path = "credentials.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =credentials_path
    translate_client = translate.Client()
    message = json["message"]
    target = json["language"]
    if isinstance(message, bytes):
        message = message.decode("utf-8")
    result = translate_client.translate(message, target_language=target)
    result["translatedText"] = html.unescape(result["translatedText"])
    return result

def translateAndConvert(json):
    response = translate_text(json)
    standard_format = {"name" : json["name"], "message" : response["translatedText"], "language" : json["language"], "timestamp" : json["timestamp"]}
    return standard_format

with open("tests/test.json") as test:
    json = json.load(test)


print(translateAndConvert(json))