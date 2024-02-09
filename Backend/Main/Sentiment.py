import json
import requests
from dotenv import load_dotenv
from Message import MessageFromClient, MessageToClient
import os


load_dotenv()


def sentiment_analysis(message: MessageFromClient):
	url = os.environ.get("URL")
	headers = {
		"X-RapidAPI-Key": os.environ.get("XKEY"),
		"X-RapidAPI-Host": os.environ.get("XHOST")
	}
	querystring = {"text": message.message}
	response = requests.get(url, headers=headers, params=querystring)
	message = message.__dict__
	message["sentiment"] = response.json()["score"]
	return MessageToClient.model_validate(message)
