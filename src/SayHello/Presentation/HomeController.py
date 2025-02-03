from flask import render_template

class HomeController:

    def __init__(self, app, message_service):

        # Curious about this? The Flask decorator on the inner function establishes a referenece to the function
        # (the function is "wrapped"), so the function is not destroyed when __init__ exits.
                
        @app.route('/')
        def home():

            result = render_template('SayHello/Presentation/home.html', message = message_service.get_message('hello'))
            return result