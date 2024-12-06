import requests
import os

def callBot(MESSAGE):
    TOKEN = os.environ['TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}"
    
    return requests.get(url).json()