from datetime import datetime
import inspect
import json
import os
import requests
import sys
import urllib

class Mimi():
    ACCESS_TOKEN = 'accesstoken'

    def __init__(self, auth):
        self.__auth = auth

    def __read_accesstoken(self):
        if not os.path.isfile(self.ACCESS_TOKEN):
            return {'endTimestamp' : 0, 'expires_in' : 0}

        with open(self.ACCESS_TOKEN, "r", encoding="utf-8") as f:
            return json.load(f)

    def __save_accesstoken(self, data):
        if os.path.isfile(self.ACCESS_TOKEN):
            os.remove(self.ACCESS_TOKEN)

        with open(self.ACCESS_TOKEN, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def __accesstoken(self):
        json_data = self.__read_accesstoken()
        if json_data['endTimestamp'] + json_data['expires_in'] > datetime.now().timestamp():
            return False, json_data['accessToken']

        scope = ''
        for v in self.__auth['scope']:
            scope += v + ';'

        res = requests.post(
            url='https://auth.mimi.fd.ai/v2/token',
            data={
                'grant_type': 'https://auth.mimi.fd.ai/grant_type/client_credentials',
                'client_id': self.__auth['applicationId'] + ':' + self.__auth['clientId'],
                'client_secret': self.__auth['clientSecret'],
                'scope' : scope.rstrip(';'),
            }
        )

        if res.status_code != 200:
            return True, f'{sys._getframe().f_code.co_name}:status is bad:{str(res.status_code)}'

        json_data = res.json()

        if json_data['status'] != 'success':
            return True, f'{sys._getframe().f_code.co_name}:Authentication is failed'

        self.__save_accesstoken(json_data)

        return False, json_data['accessToken']

    def speech(self, params):
        err, access_token = self.__accesstoken()
        if err:
            return err, access_token

        res = requests.post(
            url='https://tts.mimi.fd.ai/speech_synthesis',
            headers={
                'Authorization':  f'Bearer {access_token}',
            },
            data=params
        )

        if res.status_code != 200:
            return True, f'{sys._getframe().f_code.co_name}:status is bad:{str(res.status_code)}'

        return False, res.content
