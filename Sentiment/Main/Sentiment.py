import requests
from fastapi import FastAPI
from pydantic import BaseModel


class Sentiment:
	url = "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/"
	headers = {
		"X-RapidAPI-Key": "84a49088d0msh16c065ef4f13cc6p1b0966jsnaccf04991951",
		"X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com"
	}

	def sentiment_analysis(self, text: str) :
		querystring = {"text": text}
		response = requests.get(self.url, headers=self.headers, params=querystring)
		return response.json()


class Message(BaseModel):
	message: str
	name: str
	sentiment: str


app = FastAPI()
sentiment = Sentiment()
print(sentiment.sentiment_analysis("I hate you!"))


@app.post("/sendMessage")
def receive_message(message: Message):
	return sentiment.sentiment_analysis(message.message)
