from flask import Flask
import telegram_notification as tele
import service

app = Flask(__name__)


@app.route('/sendTeleMsg/<string:str>')
def sendMessege(str):
    return tele.callBot(str)

@app.route('/')
def hello_world():
    return service.getHistoryCalData("NSE","99926000","ONE_MINUTE","2024-11-08 09:16","2024-11-08 10:16")

# Befor pushing to git please comment the below 2 lines
if __name__ == '__main__':
    app.run()