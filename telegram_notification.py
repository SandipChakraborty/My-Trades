import requests
import os

def callBot(msg):
    token = os.environ.get('TOKEN')
    chatId = os.environ.get('CHAT_ID')
    # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatId}&text={msg}"
    return requests.get(url).json()
