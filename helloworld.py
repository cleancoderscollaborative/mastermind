import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():

    return '''
        <div style="background-color: lightgray; text-align: center; min-height: calc(100vh - (100vh - 300px) / 2); padding-top: calc((100vh - 300px) / 2);">
            <img src="/static/images/clean-code.png" /><h1>Hello World, good to go!</h1>
        </div>
    '''

service_port = os.getenv('SERVICEPORT')
domain = os.getenv('CODESPACE_NAME')

if __name__ == '__main__':

    if domain:
        print(f"Application starting on port https://{domain}-{service_port}.app.github.dev/")
    else:
        print(f"Application starting on http://localhost:{service_port}/")

    app.run(debug=True, port=service_port)