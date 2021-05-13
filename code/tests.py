import unittest
import aiogram
from get_messages import get_messages


class Test_get_message(unittest.TestCase):
    def setUp(self):
        self.message = aiogram.types.message.Message
        self.operate = get_messages
        self.possible_inputs = ["1", "Unknown_text", 'Погода сегодня', 'Погода недели', 'Новости сегодня']

    def test_wrong_answer(self):
        self.message.text = self.possible_inputs[0]
        self.assertEqual(self.operate(self.message), 'Я не знаю что ответить 😢')
        self.message.text = self.possible_inputs[1]
        self.assertEqual(self.operate(self.message), 'Я не знаю что ответить 😢')

    def test_get_today_weather(self):
        message_lenth = 7
        self.message.text = self.possible_inputs[2]
        self.assertEqual(self.operate(self.message)[0: message_lenth], "Cегодня")

    def test_get_week_weather(self):
        message_lenth = 22
        self.message.text = self.possible_inputs[3]
        self.assertEqual(self.operate(self.message)[0: message_lenth], "погода на этой неделе:")

    def test_get_today_news(self):
        message_lenth = 20
        self.message.text = self.possible_inputs[4]
        self.assertEqual(self.operate(self.message)[0: message_lenth], "Сегодняшние новости:")
