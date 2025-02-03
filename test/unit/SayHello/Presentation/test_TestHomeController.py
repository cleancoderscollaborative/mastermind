import flask
import src.SayHello.Presentation.HomeController

from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

class TestHomeController(TestCase):

    @classmethod
    def setUpClass(cls):

        #
        # See the unit test test_TestMain.py for a full description of how we hoist mocks to make these tests work.
        #

        cls.mock_flask()

        reload(src.SayHello.Presentation.HomeController)   # Reload the CUT to get the mock of Flask.

        cls.mock_route()
        cls.mock_message_service()
    
    @classmethod
    def tearDownClass(cls) -> None:

        cls.restore_message_service()
        cls.restore_route()
        cls.restore_flask()

        reload(src.SayHello.Presentation.HomeController)    # Reload the CUT to get the restored Flask.

        super().tearDownClass()
    
    def setUp(self) -> None:

        self.home_controller = src.SayHello.Presentation.HomeController.HomeController(TestHomeController.mock_app, TestHomeController.mock_message_service)

    @classmethod
    def mock_flask(cls):

        cls.mod_flask_render_template = flask.render_template
        flask.render_template = cls.mock_render_template = MagicMock()

    @classmethod
    def mock_route(cls):

        cls.mock_app = MagicMock()
        cls.mock_app.route = MagicMock()
        cls.mock_app.route.decorator = MagicMock()
        cls.mock_app.route.return_value = cls.mock_app.route.decorator

    @classmethod
    def mock_message_service(cls):

        cls.mock_message_service = MagicMock()

    @classmethod
    def restore_flask(cls):

        flask.render_template = cls.mod_flask_render_template

    @classmethod
    def restore_route(cls):
        pass

    @classmethod
    def restore_message_service(cls):
        pass

    def test_home_controller_home_path(self) -> None:

        TestHomeController.mock_app.route.assert_called_once_with('/')

    def test_home_controller_home_result(self) -> None:

        TestHomeController.mock_message_service.get_message.return_value = 'pass'
        TestHomeController.mock_render_template.return_value = 'pass'

        args, kwargs = TestHomeController.mock_app.route.decorator.call_args

        result = args[0]()      # This is the inline function to flask routes the path to, the best way find it.

        self.assertEqual('pass', result)
    
    def test_home_controller_home_render_parameters(self) -> None:

        TestHomeController.mock_message_service.get_message.return_value = 'pass message'
        TestHomeController.mock_render_template.return_value = 'pass'

        args, kwargs = TestHomeController.mock_app.route.decorator.call_args

        result = args[0]()

        TestHomeController.mock_render_template.assert_called_once_with('SayHello/Presentation/home.html', message = 'pass message')