from src.service.MessageService import MessageService

class HomeController:

    def __init__(self, app, message_service):

        self.message_service = message_service
                
        @app.route("/")
        def hello_world():

            return f'''
            <html>
            <head>
                <link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico" />
            </head>
            <body>
                <div style="background-color: lightgray; text-align: center; min-height: calc(100vh - (100vh - 300px) / 2); padding-top: calc((100vh - 300px) / 2);">
                    <img src="/assets/images/clean-code.png" /><h1>{self.message_service.get_message('hello')}</h1>
                </div>
            </body>
            </html>
            '''