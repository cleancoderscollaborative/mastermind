from flask import render_template

class HomeController:

    def __init__(self, app, message_service):

        self.message_service = message_service
                
        @app.route('/')
        def home():

            result = render_template('page/home.html', message = self.message_service.get_message('hello'))
            return result