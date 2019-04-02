import requests
import json
# import base64
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# def login_post(data_login):
#     login_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"
#     r_login = requests.post(login_url, data = data_login)
#     return r_login

# def eleme_login():
#     print('Eleme account:'),
#     eleme_acc = str(input())
#     # urls
#     get_captcha = "https://h5.ele.me/restapi/eus/v3/captchas"
#     r_login = login_post({'captcha_hash': '', 'captcha_hash': '', 'mobile': eleme_acc, 'scf': 'ms'})
#     if r_login.status_code == 200:
#         print 'success'
#     else:
#         login_resp = json.loads(r_login.text)
#         if login_resp['name'] == 'NEED_CAPTCHA':
#             r_captcha = requests.post(get_captcha, data = {'captcha_str': eleme_acc})
#             captcha_resp = json.loads(r_captcha.text)
#             captcha_img = captcha_resp['captcha_image']
#             # get image data from base64 string 
#             image_data = base64.b64decode(captcha_img[22:])
#             captcha_hash = captcha_resp['captcha_hash']
#             captcha_file_name = 'captcha_img.jpg'
#             with open(captcha_file_name, 'wb') as f:
#                 f.write(image_data)
#             img = mpimg.imread(captcha_file_name)
#             imgplot = plt.imshow(img)
#             plt.show()
#             print ('Captcha:'),
#             captcha_str = str(input())


def get_drinks_data():
    headers = {
        "Cookie":"ubt_ssid=wy12lpik1zsa8upoehbyy5c7inf6mctn_2019-04-02; _utrace=56efeb46f7b4790a648d0417670bc546_2019-04-02; cna=GaojFa/HHz0CAWXkE9XcSPdv; track_id=1554210095|1e2f0ffe2bcb0414dc538cf5c4f1007c5bd05832af0a901eeb|a772d7023d218603d977c8f4ad8ebfe3; USERID=1171026; UTUSER=1171026; SID=GM1bzQMg6zIsYMTmOy66g1dQ2g23RHFQV6IQ; isg=BDMz4DV0a3kv-Cetjhnge0KmwjGdwMYgLZhtCuXR4tKJ5FmGcDpnewK1m1yv6x8i; pizza73686f7070696e67=CPuz42fVoxnRVcVQ1x33fQ4jyT1fzkJKkcTiE3_s4oj-S8pgMw6yhQBkM8XxQctq"
    }
    # cookies = {'ubt_ssid':'wy12lpik1zsa8upoehbyy5c7inf6mctn_2019-04-02','_utrace':'56efeb46f7b4790a648d0417670bc546_2019-04-02', 'cna':'GaojFa/HHz0CAWXkE9XcSPdv','track_id':'1554210095|1e2f0ffe2bcb0414dc538cf5c4f1007c5bd05832af0a901eeb|a772d7023d218603d977c8f4ad8ebfe3','USERID':'1171026', 'UTUSER':'1171026','SID':'nYJZyfQgNqMjlyI1gcGd1Rsllf7TcFnxHvBw','isg':'BG9vOkCyb0UQt2t5KjVk9-6y_oW5vMI88QyhfoH9Pl7l0InSlObTh_FBV4jLgZuu','pizza73686f7070696e67':'CPuz42fVoxnRVcVQ1x33fd7kMud2ByAX2FS937c69gllXZo6j7xdnfKR1IjbKOyv'}
    data_resp = requests.get('https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wtw3td55ryw8&latitude=31.212751&limit=24&longitude=121.535223&offset=0&terminal=web', headers=headers)
    data_json = json.loads(data_resp.text)
    print data_resp.text


if __name__ == "__main__":
    # eleme_login()
    get_drinks_data()
