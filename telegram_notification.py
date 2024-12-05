import requests

def callBot(MESSAGE):
    TOKEN = '7579677410:AAFmbYd-HY3ln4GeMKjPieFjb2r8Fe4VIXw'
    CHAT_ID = '1449305448'
    # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}"
    
    return requests.get(url).json()