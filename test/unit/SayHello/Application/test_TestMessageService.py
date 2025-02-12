from unittest import TestCase

from src.SayHello.ApplicationLogic.MessageService import MessageService

class TestMessageService(TestCase):

    def setUp(self):
        self.messages = {
            'test_key': 'value'
        }
        self.message_service = MessageService(self.messages)

    def test_get_message_ok(self):
        result = self.message_service.get_message('test_key')
        self.assertEqual('value', result)

    def test_get_message_missing(self):
        result = self.message_service.get_message('no_message')
        self.assertIsNone(result)
