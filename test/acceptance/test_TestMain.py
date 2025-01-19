from dotenv import load_dotenv
from os import getenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from threading import Thread
from unittest import TestCase
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

from src.main import app

class TestMain(TestCase):

    @classmethod
    def launch_app(cls):

        # Use Werkzeug in the thread launched to contain the flask app and allow it to be shut down. 

        cls.server = make_server('127.0.0.1', cls.service_port, app)
        cls.server.serve_forever()

    @classmethod
    def setUpClass(cls):

        load_dotenv()

        cls.service_port = getenv('SERVICEPORT')
        cls.thread = Thread(target = cls.launch_app)
        cls.thread.start()

        options = Options()
        options.add_argument('--headless=new')  # Remove this option if you want to see the browser
        cls.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 60)

    @classmethod
    def tearDownClass(cls):

        cls.driver.quit()
        cls.server.shutdown()
        cls.thread.join()

    def test_logo(self):

        TestMain.driver.get(f'http://localhost:{TestMain.service_port}')

        result = TestMain.driver.find_element(By.XPATH, "//img[@src='/assets/images/clean-code.png']")

        self.assertIsNotNone(result)

    def test_message(self):

        TestMain.driver.get(f'http://localhost:{TestMain.service_port}')

        result = TestMain.driver.find_element(By.XPATH, "//h1[. = 'Hello world, good to go!']")

        self.assertIsNotNone(result)