import flask
import src.controller.HomeController

from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

# rom src.controller.HomeController import HomeController

class TestHomeController(TestCase):

    @classmethod
    def setUpClass(cls):

        # Injecting mocks for Python packages is difficult because of the two ways that the package may be loaded.
        # If loaded with a straight import, replacing classes or functions is straightforward, just replace the
        # attribute with a new value. But we must assume that the client code is doing an 'from module import X',
        # and in that case the client code gets the value of X before it can be mocked. Since it is a local reference
        # now in the client code, mocking the original will not change X there. Worse, we have to load the client
        # code in the test suite before the mock because Python does not have a mechanism for hoisting the mock.
        #
        # The solution is "importlib", which allows us to simulate the hoist by reloading the imported code under
        # test (CUT) after the mock has been established, which causes it to re-import its dependencies and now
        # see the mock.
        #
        # After the test we need to put things back the way they were in case something else depends on it.

        # Save the original reference to the function being mocked.

        cls.mod_flask_render_template = flask.render_template

        # Create the mock with MagicMock.

        cls.mock_render_template = MagicMock()
        flask.render_template = cls.mock_render_template

        # Reload the CUT so it re-imports things and gets the mock:

        reload(src.controller.HomeController)

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

        # As describe above, the original must be inserted back into the flask module and
        # then both modules reloaded for other test fixtures:

        flask.render_template = cls.mod_flask_render_template

        reload(flask)
        reload(src.controller.HomeController)

        return super().tearDownClass()
    
    def setUp(self):

        self.home_controller = src.controller.HomeController.HomeController(TestHomeController.mock_app, TestHomeController.mock_message_service)

    def test_home_controller_home_path(self):

        TestHomeController.mock_app.route.assert_called_once_with('/')

    def test_home_controller_home_result(self):

        TestHomeController.mock_message_service.get_message.return_value = 'pass'
        TestHomeController.mock_render_template.return_value = 'pass'

        args, kwargs = TestHomeController.mock_app.route.decorator.call_args

        result = args[0]()      # This is the inline function to flask routes the path to, the best way find it.

        self.assertEqual('pass', result)
    
    def test_home_controller_home_render_parameters(self):

        TestHomeController.mock_message_service.get_message.return_value = 'pass message'
        TestHomeController.mock_render_template.return_value = 'pass'

        args, kwargs = TestHomeController.mock_app.route.decorator.call_args

        result = args[0]()

        TestHomeController.mock_render_template.assert_called_once_with('page/home.html', message = 'pass message')