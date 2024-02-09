import unittest
from Main.Sentiment import sentiment_analysis
from Main import MessageFromClient, MessageToClient


class TestSentiment(unittest.TestCase):
    def test_sentiment_analysis(self):
        message_given = MessageFromClient(username="Matthias", message="I like that",
                                          language="EN", timestamp="15:43:33")
        message_expected = MessageToClient(username="Matthias", message="I like that",
                                           language="EN", timestamp="15:43:33", sentiment=0.85434434)
        self.assertEqual(sentiment_analysis(message_given), message_expected)

        message_given.message = "I do not like that"
        message_expected.message = "I do not like that"
        message_expected.sentiment = -0.73967217
        self.assertEqual(sentiment_analysis(message_given), message_expected)

        message_given.message = "Ok"
        message_expected.message = "Ok"
        message_expected.sentiment = 0
        self.assertEqual(sentiment_analysis(message_given), message_expected)


if __name__ == '__main__':
    unittest.main()
