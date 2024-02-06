import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Sentiment:
	url = os.environ.get("URL")
	headers = {
		"X-RapidAPI-Key": os.environ.get("XKEY"),
		"X-RapidAPI-Host": os.environ.get("XHOST")
	}

	def sentiment_analysis(self, text: str):
		querystring = {"text": text}
		response = requests.get(self.url, headers=self.headers, params=querystring)
		return response.json()
