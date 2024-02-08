import json
import requests
from dotenv import load_dotenv
from Backend.Main import MessageFromClient, MessageToClient
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

message = b'{"username":"test","message":"test message","timestamp":"14:42:21","language":"de"}'
message = message.decode('utf8')
message = json.loads(message)
message = MessageFromClient.model_validate(message)
print(sentiment_analysis(message))
