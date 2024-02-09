import unittest
import json
from translator import *
class TranslatorTest(unittest.TestCase):
    def test_translate(self):
        text ={"name" : "Philip","message" : "Hallo, Ich bin ein Bär","language" : "EN","timestamp" : 0}
        self.assertEqual(translate_text(text)["detectedSourceLanguage"], "de")
        self.assertEqual(translate_text(text)["translatedText"], "Hello, I am a bear")

        text2 = {"name": "Philip", "message": "Hallo, Ich bin ein Bär", "language": "ES", "timestamp": 0}
        self.assertEqual(translate_text(text2)["detectedSourceLanguage"], "de")
        self.assertEqual(translate_text(text2)["translatedText"], "hola soy un oso")

    def test_translateAndConvert(self):
        text = {"name": "Philip", "message": "Hallo, Ich bin ein Bär", "language": "EN", "timestamp": 0}
        self.assertEqual(translate_and_convert(text)["name"],text["name"])
        self.assertEqual(translate_and_convert(text)["language"],text["language"])
        self.assertEqual(translate_and_convert(text)["timestamp"],text["timestamp"])
        self.assertEqual(translate_and_convert(text)["message"], "Hello, I am a bear")

if __name__ == '__main__':
    unittest.main()