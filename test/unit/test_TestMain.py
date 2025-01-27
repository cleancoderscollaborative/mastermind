import dotenv
import io
import os
import flask

from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

import src.SayHello.HomeController
import src.SayHello.messageModel
import src.SayHello.MessageService

import src.main

class TestMain(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # It is unrealistic to expect that dependencies will expect Python modules like sys or flask to be injected.
        # These modules will be imported in one of two ways: import <module> or from <module> import <component>.
        # In the first case mocking a component is straightforward, just use patch to change what it does.
        #
        # Unfortunately we must assume that the client code is using the more popular second form, because that
        # brings in just what you need by name. When this form is used, the local name is a copy of the reference
        # to the original component, so mocking the module does ot work when the dependency is still using the
        # original reference. Also unfortunately, Python has does not implement "hoisting" directly to
        # replace an imported component.
        # 
        # The solution is "importlib", which allows us to simulate a hoist by reloading the code under
        # test (CUT) after the mock has been established, which causes it to re-import the reference and pick
        # up the mock reference instead. Because of the overhead we do this once in setUpClass in front of all
        # the tests replacing the components with MagicMock instances, and then adjust the mocks in individual
        # tests as necessary.
        #
        # In the test suite we often import the whole module; for example here we import fthe whole lask module so
        # we can get to the components that need to be mocked. Patch does not often help here because of the
        # hierarchial structure of what is being used. Here we build that with MagicMock instances and do a
        # direct replacement.
        #
        # After the tests we need to put the mocked components back the way they were in case some other code depending
        # on it needs it to work the something else depends on it, so look to the tearDownClass method.
        #

        # Save the original reference to the components being mocked.

        cls.mod_dotenv_load_dotenv = dotenv.load_dotenv
        cls.mod_flask_Flask_class = flask.Flask
        cls.mod_os_getenv = os.getenv
        cls.mod_src_controller_HomeController_class = src.SayHello.HomeController.HomeController
        cls.mod_src_model_messages_messages = src.SayHello.messageModel.messages
        cls.mod_src_service_MessageService_class = src.SayHello.MessageService.MessageService

        # Mock dotenv load.

        dotenv.load_dotenv = cls.mock_dotenv_load_dotenv = MagicMock()

        # Mock the Flask class and the app created from the class.

        flask.Flask = cls.mock_flask_Flask_class = MagicMock()
        cls.mock_flask_app = MagicMock()
        cls.mock_flask_Flask_class.return_value = cls.mock_flask_app

        # Mock the environment values and the service to call them.

        cls.mock_environment = { 'SERVICEPORT': '5555', 'CODESPACE_NAME' : 'wonderful-widgets', 'TEST_RUN_PIPE': os.getenv('TEST_RUN_PIPE') }

        def getenv(key):
            return cls.mock_environment.get(key)

        os.getenv = cls.mock_os_getenv = getenv

        # Mock the message dictionary, the MessageService class, and the service created from the class.

        src.SayHello.messageModel.messages = cls.mock_src_model_messages_messages = { }
        src.SayHello.MessageService.MessageService = cls.mock_src_service_MessageService_class = MagicMock()
        cls.mock_src_service_MessageService_service = MagicMock()
        cls.mock_src_service_MessageService_class.return_value = cls.mock_src_service_MessageService_service

        # Mock the HomeConroller class and the instance created.

        src.SayHello.HomeController.HomeController = cls.mock_src_controller_HomeController_class = MagicMock()
        cls.mock_src_controller_HomeController_controller = MagicMock()
        cls.mock_src_controller_HomeController_class.return_value = cls.mock_src_controller_HomeController_controller

        # Reload the CUT so it re-imports things and gets the mock:

        reload(src.main)

        # Patch stdout to check messages

        cls.mock_stdout_context = patch('sys.stdout', new_callable=io.StringIO)
        cls.mock_stdout_context.start()
    
    @classmethod
    def tearDownClass(cls) -> None:

        cls.mock_stdout_context.stop()

        # Replace the original comopnents and reload.

        dotenv.load_dotenv = cls.mod_dotenv_load_dotenv
        flask.Flask = cls.mod_flask_Flask_class
        os.getenv = cls.mod_os_getenv
        src.SayHello.HomeController.HomeController = cls.mod_src_controller_HomeController_class
        src.SayHello.messageModel.messages = cls.mod_src_model_messages_messages
        src.SayHello.MessageService.MessageService = cls.mod_src_service_MessageService_class

        reload(src.main)

        super().tearDownClass()

    def setUp(self) -> None:

        # Reset the mocks.

        TestMain.mock_dotenv_load_dotenv.reset_mock()
        TestMain.mock_flask_Flask_class.reset_mock()
        TestMain.mock_flask_app.reset_mock()
        TestMain.mock_src_controller_HomeController_class.reset_mock()
        TestMain.mock_src_controller_HomeController_controller = MagicMock()

    def test_loads_environment(self) -> None:

        src.main.start()

        TestMain.mock_dotenv_load_dotenv.assert_called_once()

    def test_creates_flask_app(self) -> None:

        src.main.start()

        TestMain.mock_flask_Flask_class.assert_called()

    def test_initializes_home_controller(self) -> None:

        src.main.start()

        TestMain.mock_src_controller_HomeController_class.assert_called_once_with(TestMain.mock_flask_app, TestMain.mock_src_service_MessageService_service)

    def test_run_flask(self) -> None:

        src.main.start()

        TestMain.mock_flask_app.run.assert_called_once_with(port = TestMain.mock_environment.get('SERVICEPORT'))

    def test_service_start_message_with_codespace(self) -> None:
        
        expected = f'https://{os.getenv("CODESPACE_NAME")}-{os.getenv("SERVICEPORT")}'

        src.main.start()

        self.assertIn(expected, TestMain.mock_stdout_context.target.stdout.getvalue())

    def test_service_start_message_without_codespace(self) -> None:

        original_codespace_name = TestMain.mock_environment.get('CODESPACE_NAME')

        TestMain.mock_environment['CODESPACE_NAME'] = None
        expected = f'http://localhost:{os.getenv("SERVICEPORT")}'

        src.main.start()

        TestMain.mock_environment['CODESPACE_NAME'] = original_codespace_name

        self.assertIn(expected, TestMain.mock_stdout_context.target.stdout.getvalue())