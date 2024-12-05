from flask import Flask
import telegram_notification as tele

app = Flask(__name__)


@app.route('/sendTeleMsg/<string:str>')
def sendMessege(str):
    return tele.callBot(str)

@app.route('/')
def hello_world(str):
    return "Hi There"

# Befor pushing to git please comment the below 2 lines
# if __name__ == '__main__':
#     app.run()