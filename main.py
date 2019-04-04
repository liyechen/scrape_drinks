import requests
import json
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def login_post(data_login):
    login_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"
    r_login = requests.post(login_url, data = data_login)
    return r_login

def eleme_login():
    print('Eleme account:', end=',')
    eleme_acc = str(input())
    # urls
    get_captcha = "https://h5.ele.me/restapi/eus/v3/captchas"
    r_login = login_post({'captcha_hash': '', 'captcha_hash': '', 'mobile': eleme_acc, 'scf': 'ms'})
    if r_login.status_code == 200:
        print('success')
    else:
        login_resp = json.loads(r_login.text)
        if login_resp['name'] == 'NEED_CAPTCHA':
            r_captcha = requests.post(get_captcha, data = {'captcha_str': eleme_acc})
            captcha_resp = json.loads(r_captcha.text)
            captcha_img = captcha_resp['captcha_image']
            # get image data from base64 string 
            image_data = base64.b64decode(captcha_img[22:])
            captcha_hash = captcha_resp['captcha_hash']
            captcha_file_name = 'captcha_img.jpg'
            with open(captcha_file_name, 'wb') as f:
                f.write(image_data)
            img = mpimg.imread(captcha_file_name)
            imgplot = plt.imshow(img)
            plt.show()
            print ('Captcha:'),
            captcha_str = str(input())

if __name__ == "__main__":
    eleme_login()
