import unittest
import aiogram
from get_messages import get_messages


class Test_get_message(unittest.TestCase):
    def setUp(self):
        self.message = aiogram.types.message.Message
        self.operate = get_messages

    def test_wrong_answer(self):
        self.message.text = "1"
        self.assertEqual(self.operate(self.message), 'Я не знаю что ответить 😢')
        self.message.text = "Unknown_text"
        self.assertEqual(self.operate(self.message), 'Я не знаю что ответить 😢')

    def test_get_today_weather(self):
        self.message.text = 'Погода сегодня'
        self.assertEqual(self.operate(self.message)[0: 7], "Cегодня")

    def test_get_week_weather(self):
        self.message.text = 'Погода недели'
        self.assertEqual(self.operate(self.message)[0: 22], "погода на этой неделе:")

    def test_get_today_news(self):
        self.message.text = 'Новости сегодня'
        self.assertEqual(self.operate(self.message)[0: 20], "Сегодняшние новости:")
