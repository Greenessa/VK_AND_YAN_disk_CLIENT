# Программа копирует фотографии с профиля VK и записывает их в отдельную папку на яндекс диск.
# Предварительно получается токен для доступа к фотографиям в контакте и OAUTH token для доступа в яндекс диск
import time
from tqdm import tqdm
import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A warning")
logging.error("An error")
logging.critical("A message of critical severnity")

import requests
from pprint import pprint
# from urllib.parse import urlencode
#
# Oauth_Base_url = 'https://oauth.vk.com/authorize'
# params = {'client_id': '51722110', 'redirect_uri': 'https://oauth.vk.com/blank.html', 'display': 'page', 'scope': 'photos', 'response_type': 'token', 'v':'5.131', 'state': '123456'}
# auth_url = f'{Oauth_Base_url}?{urlencode(params)}'
# print(auth_url)

class VK_Client:
    API_BASE_URL = 'https://api.vk.com/method'
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_params(self):
        return {'access_token': self.token, 'v': '5.131'}
    def get_photos(self):
        params = self.get_params()
        params.update({'owner_id': self.user_id, "extended": 1})
        resp = requests.get(f'{self.API_BASE_URL}/photos.getAll', params=params).json()
        #pprint(resp)
        return resp
    

token1 = open('token1').read()
vk_klient_my = VK_Client(token1, 815147892)
dict = vk_klient_my.get_photos()
pprint(dict)


class Yandex_Client:

    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': 'OAuth ' + token}
    def create_folder(self, path_name_folder):
        # Создаём папку на яндекс диске
        #headers = {'Authorization': 'OAuth ' + token}
        params = {'path': path_name_folder}
        res_folder = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=self.headers, params=params)
        print(res_folder.status_code)
        print(res_folder.json())
    def upload_photos(self, dict, path_name_folder):
        # загружаем файлы на Яндекс диск
        params = {'path': path_name_folder}
        for item in tqdm(dict['response']['items']):
            for size in item['sizes']:
                if size['type'] == 'w':
                    #print(size['url'])
                    params = {'path': f'{path_name_folder}/{item["likes"]["count"]}', 'url': size['url']}
                    responce = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=self.headers, params=params)
                    print(responce.status_code)
                    print(responce.json())
            time.sleep(1)


token = open("token").read()
yandex_cl1 = Yandex_Client(token)
yandex_cl1.create_folder('/photos_from_vk')
yandex_cl1.upload_photos(dict, '/photos_from_vk')