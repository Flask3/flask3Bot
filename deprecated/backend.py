from flask import Flask
from bot_main import main # this will be your file name; minus the `.py`

app = Flask(__name__)

@app.route('/')
def dynamic_page():
    file = open('bot_main.py', 'r').read()
    return exec(file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)