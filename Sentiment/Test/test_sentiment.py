import unittest
from Sentiment.Main.Sentiment import Sentiment


class TestSentiment(unittest.TestCase):
    def test_sentiment_analysis(self):
        sentiment = Sentiment()
        self.assertEqual(sentiment.sentiment_analysis("I like that")["type"], "positive")  # add assertion here
        self.assertEqual(sentiment.sentiment_analysis("I do not like that")["type"], "negative")
        self.assertEqual(sentiment.sentiment_analysis("Ok")["type"], "neutral")
        self.assertEqual(sentiment.sentiment_analysis("I like that")["score"], 0.85434434)  # add assertion here
        self.assertEqual(sentiment.sentiment_analysis("I do not like that")["score"], -0.73967217)
        self.assertEqual(sentiment.sentiment_analysis("Ok")["score"], 0)


if __name__ == '__main__':
    unittest.main()
