import os
import requests
from dotenv import load_dotenv

from Backend.Main import Message

load_dotenv()


def sentiment_analysis(message: Message):
	url = os.environ.get("URL")
	headers = {
		"X-RapidAPI-Key": os.environ.get("XKEY"),
		"X-RapidAPI-Host": os.environ.get("XHOST")
	}
	querystring = {"text": message.message}
	response = requests.get(url, headers=headers, params=querystring)
	message.sentiment = response.json()["score"]
	return message

message = Message(name="Philip", message="Hello I am a bear", language="EN", timestamp="11:24:39", sentiment=0.0)

print(sentiment_analysis(message))
