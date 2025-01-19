from unittest import TestCase
from xml.etree import ElementTree

from src.main import app

class TestMain(TestCase):

    @classmethod
    def setUpClass(cls):

        # Be aware that the app is created by main so there is one copy for all tests, and therefore
        # one test client.

        cls.client = app.test_client()

    def test_page_ok(self):

        response = TestMain.client.get('/')

        self.assertEqual(200, response.status_code)

    def test_page_html(self):

        response = TestMain.client.get('/')

        self.assertIn('text/html', response.content_type)

    def test_logo(self):

        response = TestMain.client.get('/')
        print(response.text)

        root = ElementTree.fromstring(response.text)
        result = root.find(".//img[@src='/assets/images/clean-code.png']")

        self.assertIsNotNone(result)

    def test_message(self):

        response = TestMain.client.get('/')
        print(response.text)

        root = ElementTree.fromstring(response.text)
        result = root.find(".//h1[. = 'Hello world, good to go!']")

        self.assertIsNotNone(result)