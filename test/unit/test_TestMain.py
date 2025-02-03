import dotenv
import io
import os
import flask

from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

import src.SayHello.Presentation.HomeController
import src.SayHello.Domain.messageModel
import src.SayHello.Application.MessageService

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

        cls.mock_dotenv()
        cls.mock_flask()
        cls.mock_os()
        cls.mock_HomeConroller()
        cls.mock_messages()
        cls.mock_MessageService()

        reload(src.main)    # Reload the module to get the new references.

        cls.patch_stdout()
    
    @classmethod
    def tearDownClass(cls) -> None:

        cls.restore_stdout()

        cls.restore_dotenv()
        cls.restore_flask()
        cls.restore_os()
        cls.restore_HomeController()
        cls.restore_messages()
        cls.restore_MessageService()

        reload(src.main)    # Reload the module to get the restored references.

        super().tearDownClass()

    def setUp(self) -> None:

        # Reset the mocks before each test.

        TestMain.mock_dotenv_load_dotenv.reset_mock()
        TestMain.mock_flask_Flask_class.reset_mock()
        TestMain.mock_flask_app.reset_mock()
        TestMain.mock_src_presentation_HomeController_class.reset_mock()
        TestMain.mock_src_presentation_HomeController_controller = MagicMock()

    @classmethod
    def mock_dotenv(cls):

        cls.mod_dotenv_load_dotenv = dotenv.load_dotenv
        dotenv.load_dotenv = cls.mock_dotenv_load_dotenv = MagicMock()

    @classmethod
    def mock_flask(cls):

        cls.mod_flask_Flask_class = flask.Flask
        flask.Flask = cls.mock_flask_Flask_class = MagicMock()
        cls.mock_flask_app = MagicMock()
        cls.mock_flask_Flask_class.return_value = cls.mock_flask_app

    @classmethod
    def mock_os(cls):

        cls.mod_os_getenv = os.getenv
        
        cls.mock_environment = { 'SERVICEPORT': '5555', 'CODESPACE_NAME' : 'wonderful-widgets', 'TEST_RUN_PIPE': os.getenv('TEST_RUN_PIPE') }

        def getenv(key):
            return cls.mock_environment.get(key)

        os.getenv = cls.mock_os_getenv = getenv

    @classmethod
    def mock_HomeConroller(cls):

        cls.mod_src_presentation_HomeController_class = src.SayHello.Presentation.HomeController.HomeController
        src.SayHello.Presentation.HomeController.HomeController = cls.mock_src_presentation_HomeController_class = MagicMock()
        cls.mock_src_presentation_HomeController_controller = MagicMock()
        cls.mock_src_presentation_HomeController_class.return_value = cls.mock_src_presentation_HomeController_controller

    @classmethod
    def mock_messages(cls):

        cls.mod_src_domain_messages_messages = src.SayHello.Domain.messageModel.messages
        src.SayHello.Domain.messageModel.messages = cls.mock_src_domain_messages_messages = { }

    @classmethod
    def mock_MessageService(cls):

        cls.mod_src_application_MessageService_class = src.SayHello.Application.MessageService.MessageService
        src.SayHello.Application.MessageService.MessageService = cls.mock_src_application_MessageService_class = MagicMock()
        cls.mock_src_application_MessageService_service = MagicMock()
        cls.mock_src_application_MessageService_class.return_value = cls.mock_src_application_MessageService_service

    @classmethod
    def patch_stdout(cls):

        cls.mock_stdout_context = patch('sys.stdout', new_callable=io.StringIO)
        cls.mock_stdout_context.start()

    @classmethod
    def restore_dotenv(cls):

        dotenv.load_dotenv = cls.mod_dotenv_load_dotenv

    @classmethod
    def restore_flask(cls):

        flask.Flask = cls.mod_flask_Flask_class

    @classmethod
    def restore_os(cls):

        os.getenv = cls.mod_os_getenv

    @classmethod
    def restore_HomeController(cls):

        src.SayHello.Presentation.HomeController.HomeController = cls.mod_src_presentation_HomeController_class

    @classmethod
    def restore_messages(cls):

        src.SayHello.Domain.messageModel.messages = cls.mod_src_domain_messages_messages

    @classmethod
    def restore_MessageService(cls):

        src.SayHello.Application.MessageService.MessageService = cls.mod_src_application_MessageService_class

    @classmethod
    def restore_stdout(cls):

        cls.mock_stdout_context.stop()

    def test_loads_environment(self) -> None:

        src.main.start()

        TestMain.mock_dotenv_load_dotenv.assert_called_once()

    def test_creates_flask_app(self) -> None:

        src.main.start()

        TestMain.mock_flask_Flask_class.assert_called()

    def test_initializes_home_controller(self) -> None:

        src.main.start()

        TestMain.mock_src_presentation_HomeController_class.assert_called_once_with(TestMain.mock_flask_app, TestMain.mock_src_application_MessageService_service)

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