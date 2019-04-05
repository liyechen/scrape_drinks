import requests
import json
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import geohash

def get_place_code(lat, lon):
    return geohash.encode(lat, lon, 12)

def get_restaurants_url(lat, lon):
    place_code = get_place_code(lat, lon)
    url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=" + place_code + "&latitude=" + lat + "&limit=200&longitude=" + lon + "&offset=0&terminal=web"

def get_restaurants(place_code, cookies):
    url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wtw3sz12nxzf&latitude=31.239666&limit=200&longitude=121.499809&offset=0&terminal=web"
    resp = requests.get(url, cookies = cookies)
    restaurants = json.loads(resp.text)
    print (type(restaurants))
    print (len(restaurants))

def login_post(eleme_acc, captcha_hash, captcha_value):
    login_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"
    r_login = requests.post(login_url, data = {'captcha_hash': captcha_hash, 'captcha_value': captcha_value, 'mobile': eleme_acc, 'scf': 'ms'})
    return r_login

def eleme_login_to_get_cookies():
    print('Eleme account:')
    eleme_acc = str(input())
    # urls
    get_captcha = "https://h5.ele.me/restapi/eus/v3/captchas"
    r_login = login_post(eleme_acc, '', '')
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
            captcha_value = str(input())
            captcha_login = login_post(eleme_acc, captcha_hash, captcha_value)
            captcha_json = json.loads(captcha_login.text)
            print (captcha_json)
            validate_token = captcha_json['validate_token']
            print ('validate code:')
            validate_code = str(input())
            mobile_url = "https://h5.ele.me/restapi/eus/login/login_by_mobile"
            validate_resp = requests.post(mobile_url, data = {'mobile': eleme_acc, 'scf': 'ms', 'validate_code': validate_code, 'validate_token': validate_token})
            cookies_json = json.loads(validate_resp.cookies)
            print (cookies_json)



def get_eleme_cookies():
    f = open('eleme_cookie.txt')
    data = str(f.read())
    datas = data.split('; ')
    cookies = {}
    for key_value in datas:
        [key, value] = key_value.split('=')
        if value.endswith('\n'):
            value = value[:len(value) - 1]
        cookies[key] = value
    return cookies

if __name__ == "__main__":
    # eleme_cookies = get_eleme_cookies()
    eleme_login_to_get_cookies()
    # get_restaurants('', eleme_cookies)
