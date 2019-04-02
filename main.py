import requests
import json

def eleme_login():
    print('Eleme account:'),
    eleme_acc = str(input())
    login_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"
    r = requests.post(login_url, data = {'captcha_hash': '', 'captcha_hash': '', 'mobile': eleme_acc, 'scf': 'ms'})
    login_resp = json.loads(r.text)
    print login_resp['name']


if __name__ == "__main__":
    eleme_login()
