from flask import render_template

from src.service.MessageService import MessageService

class HomeController:

    def __init__(self, app, message_service):

        self.message_service = message_service
                
        @app.route("/")
        def hello_world():

            return render_template('page/home.html', message = self.message_service.get_message('hello'))