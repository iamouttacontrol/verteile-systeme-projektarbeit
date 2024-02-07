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

def translate_and_convert(json):
    response = translate_text(json)
    standard_format = {"name" : json["name"], "message" : response["translatedText"], "language" : json["language"], "timestamp" : json["timestamp"]}
    return standard_format


text = {
  "name" : "Philip",
  "message" : "Hallo, Ich bin ein Bär",
  "language" : "EN",
  "timestamp" : 0
}


print(translate_and_convert(text))