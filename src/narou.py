import json
import requests
import sys
import urllib

class Narou():
    def __init__(self, order):
        self.__order = order

    def getrank(self):
        params = {
            'out': 'json',
            'of': 't-s', # t:title,s:story
            'lim': '5',
            'order': self.__order,
        }

        url = '{}?{}'.format('https://api.syosetu.com/novelapi/api/', urllib.parse.urlencode(params))
        res = requests.get(url=url)

        if res.status_code != 200:
            return True, f'{sys._getframe().f_code.co_name}:status is bad:{str(res.status_code)}'

        return False, res.json()

