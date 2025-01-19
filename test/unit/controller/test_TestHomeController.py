import flask

from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.controller.HomeController import HomeController

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

        # Replace the original function with the mock, and start the mock.

        cls.mock_flask_render_template_context = patch('flask.render_template', return_value = cls.mock_render_template)
        cls.mock_flask_render_template_context.start()

        # Reload the CUT so it re-imports things and gets the mock:

        reload(HomeController)
    
    @classmethod
    def tearDownClass(cls) -> None:

        # Stop the mock context.

        cls.mock_flask_render_template_context.stop()

        # As describe above, the original must be inserted back into the flask module and
        # then both modules reloaded for other test fixtures:

        flask.render_template = cls.mod_render_template

        reload(flask)
        reload(HomeController)

        return super().tearDownClass()
