import requests
from spaceone.core.connector import BaseConnector

class TokenConnector(BaseConnector):

    def get_access_token(self, params, headers):
        r = requests.post('https://auth.worksmobile.com/oauth2/v2.0/token', data=params, headers=headers)
        json_result = r.json()
        # print(json_result['refresh_token'])
        return json_result['access_token']