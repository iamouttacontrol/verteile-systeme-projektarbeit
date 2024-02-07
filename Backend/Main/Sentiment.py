import os
import requests
from dotenv import load_dotenv

load_dotenv()


def sentiment_analysis(text: str):
	url = os.environ.get("URL")
	headers = {
		"X-RapidAPI-Key": os.environ.get("XKEY"),
		"X-RapidAPI-Host": os.environ.get("XHOST")
	}
	querystring = {"text": text}
	response = requests.get(url, headers=headers, params=querystring)
	return response.json()
