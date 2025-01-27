import flask
import src.SayHello.HomeController

from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

class TestHomeController(TestCase):

    @classmethod
    def setUpClass(cls):

        #
        # See the unit test test_TestMain.py for a full description of how we hoist mocks to make these tests work.
        #

        # Save the original reference to the function being mocked.

        cls.mod_flask_render_template = flask.render_template

        # Create the mock with MagicMock.

        flask.render_template = cls.mock_render_template = MagicMock()

        # Reload the CUT so it re-imports things and gets the mock:

        reload(src.SayHello.HomeController)

        # We also need need mock the route decorator for the app object, and check that the correct routes are specified
        # and linked to the correct methods. Fortunately, the HomeController expects the app object to be injected so we
        # do not need a real one.
        
        cls.mock_app = MagicMock()
        cls.mock_app.route = MagicMock()
        cls.mock_app.route.decorator = MagicMock()
        cls.mock_app.route.return_value = cls.mock_app.route.decorator
        cls.mock_message_service = MagicMock()
    
    @classmethod
    def tearDownClass(cls) -> None:

        # Replace the original components and reload.

        flask.render_template = cls.mod_flask_render_template
        reload(src.SayHello.HomeController)

        super().tearDownClass()
    
    def setUp(self) -> None:

        self.home_controller = src.SayHello.HomeController.HomeController(TestHomeController.mock_app, TestHomeController.mock_message_service)

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

        TestHomeController.mock_render_template.assert_called_once_with('SayHello/home.html', message = 'pass message')