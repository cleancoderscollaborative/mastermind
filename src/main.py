import os
import sys

from flask import Flask
from dotenv import load_dotenv

from src.controller.HomeController import HomeController
from src.model.messages import messages
from src.service.MessageService import MessageService

load_dotenv()

app = Flask(__name__, static_folder='../static', static_url_path='/assets')
message_service = MessageService(messages)
homeController = HomeController(app, message_service)

service_port = os.getenv('SERVICEPORT')
domain = os.getenv('CODESPACE_NAME')

def start():

    debug = False

    if sys.gettrace() is not None:

        debug = True

    if domain:
        print(f"Application starting on port https://{domain}-{service_port}.app.github.dev/")
    else:
        print(f"Application starting on http://localhost:{service_port}/")

    app.run(debug = debug, port = service_port)

if __name__ == '__main__':

    start()