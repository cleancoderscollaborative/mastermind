from dotenv import load_dotenv
from flask import Flask
from os import getenv

from src.SayHello.HomeController import HomeController
from src.SayHello.messageModel import messages
from src.SayHello.MessageService import MessageService

def initialize() -> Flask:

    load_dotenv()

    # The template folder is the source folder so that pages can be placed in the feature folders.

    app = Flask(__name__, static_folder = './_assets', static_url_path = '/assets', template_folder = '.')

    message_service = MessageService(messages)

    global _home_controller  # This protects the controller from garbage collection by placing the reference in global space.
    _home_controller = HomeController(app, message_service)

    return app

def start():

    app = initialize()

    service_port = getenv('SERVICEPORT')
    domain = getenv('CODESPACE_NAME')           # The service is Codespace-aware.

    if domain:
        print(f"Application starting on port https://{domain}-{service_port}.app.github.dev/")
    else:
        print(f"Application starting on http://localhost:{service_port}/")

    app.run(port = service_port)

if __name__ == '__main__':

    start()