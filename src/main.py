from dotenv import load_dotenv
from flask import Flask
from os import getenv

from src.SayHello.Presentation.HomeController import HomeController
from src.SayHello.Domain.messageModel import messages
from src.SayHello.ApplicationLogic.MessageService import MessageService

def initialize() -> Flask:
    global _home_controller
    (app, message_service) = create_flask_app()
    _home_controller = HomeController(app, message_service)
    return app

def create_flask_app():
    load_dotenv()
    app = Flask(__name__, static_folder = './FluxServerFramework/assets', static_url_path = '/assets', template_folder = '.')
    message_service = MessageService(messages)
    return (app, message_service)


def start():
    app = initialize()
    (service_port, domain) = (getenv('SERVICEPORT'), getenv('CODESPACE_NAME'))
    print_codespace_url(domain, service_port) if domain else print_url(service_port)
    app.run(port = service_port)

def print_codespace_url(domain, service_port):
    print(f"Application starting on port https://{domain}-{service_port}.app.github.dev/")

def print_url(service_port):
    print(f"Application starting on http://localhost:{service_port}/")

if __name__ == '__main__':
    start()
