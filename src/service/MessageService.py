from src.model.messages import messages

class MessageService:

    def __init__(self, messages):

        self.messages = messages;

    def get_message(self, key):

        return self.messages.get(key)