import unittest
import json

from Backend.Main import Message
from Backend.Main.Translator import translate_text


class TranslatorTest(unittest.TestCase):
    def test_translate(self):
        message = Message(name="Philip", message="Hallo, Ich bin ein Bär", language="EN", timestamp="11:24:39", sentiment=0.0)
        self.assertEqual(translate_text(message)["detectedSourceLanguage"], "de")
        self.assertEqual(translate_text(message)["translatedText"], "Hello, I am a bear")

        message.language = "ES"
        self.assertEqual(translate_text(message)["detectedSourceLanguage"], "de")
        self.assertEqual(translate_text(message)["translatedText"], "hola soy un oso")

 #   def test_translateAndConvert(self):
 #       text = {"name": "Philip", "message": "Hallo, Ich bin ein Bär", "language": "EN", "timestamp": 0}
 #       self.assertEqual(translate_and_convert(text)["name"],text["name"])
 #       self.assertEqual(translate_and_convert(text)["language"],text["language"])
 #       self.assertEqual(translate_and_convert(text)["timestamp"],text["timestamp"])
 #       self.assertEqual(translate_and_convert(text)["message"], "Hello, I am a bear")

if __name__ == '__main__':
    unittest.main()
