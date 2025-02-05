from unittest import TestCase

from src.SayHello.Domain.messageModel import messages
from src.SayHello.ApplicationLogic.MessageService import MessageService

class TestMessageService(TestCase):

    def setUp(self):

        self.message_service = MessageService(messages)

    def test_get_message_ok(self):

        result = self.message_service.get_message('hello')

        self.assertEqual('Hello world, good to go!', result)

    def test_get_message_missing(self):

        result = self.message_service.get_message('no_message')

        self.assertIsNone(result)