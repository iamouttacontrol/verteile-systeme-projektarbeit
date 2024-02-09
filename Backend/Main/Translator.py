import os
import html
from google.cloud import translate_v2 as translate

from Message import MessageFromClient, MessageToClient


def translate_text(message: MessageFromClient | MessageToClient):
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
