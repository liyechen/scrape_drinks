import requests
import json
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import geohash
import numpy
import xlwt

def get_place_code(lat, lon):
    return geohash.encode(lat, lon, 12)

def read_shops():
    f = open('shops.txt')
    data = str(f.read())
    shops = data.split('\n')
    return shops


def get_restaurants_url(lat, lon):
    place_code = get_place_code(lat, lon)
    url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=" + place_code + "&latitude=" + lat + "&limit=200&longitude=" + lon + "&offset=0&terminal=web"

def get_restaurants_by_keyword(keyword, lat, lon, cookies):
    place_code = get_place_code(lat, lon)
    url = "https://www.ele.me/restapi/shopping/restaurants/search?extras%5B%5D=activity&keyword=" + keyword + "&latitude=" + str(lat) + "&limit=100&longitude=" + str(lon) + "&offset=0&terminal=web"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',

    }
    resp = requests.get(url, headers = headers, cookies = cookies)
    data = resp.text
    print ('text:', data)
    # data = data.replace('False', 'false')
    # data = data.replace('True', 'true')
    # data = data.replace('\"', '\\\"')
    # data = data.replace('\'', '\"')
    resp_json = json.loads(data)
    print ('resp_json:', resp_json)
    restaurants_with_food = resp_json['restaurant_with_foods']
    return restaurants_with_food

def get_restaurants(place_code, cookies):
    url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wtw3sz12nxzf&latitude=31.239666&limit=200&longitude=121.499809&offset=0&terminal=web"
    resp = requests.get(url, cookies = cookies)
    restaurants = json.loads(resp.text)
    print (restaurants)
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
            
            print (validate_resp.cookies)
            return validate_resp.cookies



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
    # fake login for cookies
    cookies = requests.cookies.RequestsCookieJar()
    login_cookies = eleme_login_to_get_cookies()
    cookies.update(login_cookies)

    # get_restaurants('', cookies)

    # shanghai's border
    west_lat = 31.1505322076
    east_lat = 30.8927974775
    north_lon = 121.5046691895
    south_lon = 121.3302612305


    # restaurants_with_food = get_restaurants_by_keyword('1点点', 31.5, 121.4122, cookies)
    # print (restaurants_with_food)
    # set for place code
    place_set = set()

    
    # prepare the xls
    xlwt_file = xlwt.Workbook()

    # read shops from shops.txt
    shops = read_shops()

    # start scraping by shop & places
    for shop in shops:
        if not shop == '':
            table = xlwt_file.add_sheet(shop, cell_overwrite_ok = True)
            shop_data = []
            shop_ids = set()
            table.write(0, 0, 'name')
            table.write(0, 1, 'address')
            table.write(0, 2, 'rating')
            table.write(0, 3, 'rating_count')
            table.write(0, 4, 'recent_order_num')
        
            i = 1
            for lat in numpy.linspace(east_lat, west_lat, 20):
                for lon in numpy.linspace(south_lon, north_lon, 20):
                    restaurants_with_food = get_restaurants_by_keyword(shop, lat, lon, cookies)
                    print (restaurants_with_food)
                    for rwf in restaurants_with_food:
                        restaurant = rwf['restaurant']
                        if not restaurant['authentic_id'] in shop_ids:
                            shop_ids.add(restaurant['authentic_id'])
                            address = restaurant['address']
                            name = restaurant['name']
                            rating = restaurant['rating']
                            rating_count = restaurant['rating_count']
                            recent_order_num = restaurant['recent_order_num']
                            table.write(i, 0, name)
                            table.write(i, 1, address)
                            table.write(i, 2, rating)
                            table.write(i, 3, rating_count)
                            table.write(i, 4, recent_order_num)
                            i = i + 1
    
    xlwt_file.save('data.xls')
                        


    # xlwt_file = xlwt.Workbook()

    # table = xlwt_file.add_sheet('1diandian', cell_overwrite_ok = True)
    # f = open('test.txt')
    # data = str(f.read())
    # data = data.replace('False', 'false')
    # data = data.replace('True', 'true')
    # data = data.replace('\"', '\\\"')
    # data = data.replace('\'', '\"')
    # data_json = json.loads(data)
    # rwfs = data_json['restaurant_with_foods']
    # i = 0
    # table.write(i, 0, 'name')
    # table.write(i, 1, 'address')
    # table.write(i, 2, 'rating')
    # table.write(i, 3, 'rating_count')
    # table.write(i, 4, 'recent_order_num')
    # i = 1
    # for rfw in rwfs:
    #     restaurant = rfw['restaurant']
    #     address = restaurant['address']
    #     name = restaurant['name']
    #     rating = restaurant['rating']
    #     rating_count = restaurant['rating_count']
    #     recent_order_num = restaurant['recent_order_num']
    #     table.write(i, 0, name)
    #     table.write(i, 1, address)
    #     table.write(i, 2, rating)
    #     table.write(i, 3, rating_count)
    #     table.write(i, 4, recent_order_num)
    #     i = i + 1
    # xlwt_file.save('data.xls')
