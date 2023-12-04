import json
import requests
import logging
from spaceone.core.connector import BaseConnector

from plugin.error.https import ERROR_CLIENT_REQUEST_FAILED, ERROR_SERVER_FAILED

_LOGGER = logging.getLogger(__name__)


class NaverWorksConnector(BaseConnector):

    def send_message(self, bot_id: str, channel_id: str, data: dict, headers: dict) -> None:
        url = f'https://www.worksapis.com/v1.0/bots/{bot_id}/channels/{channel_id}/messages'
        print(json.dumps(data))
        res = requests.post(url, data=json.dumps(data), headers=headers)

        if res.status_code != 201:
            self._handle_https_error(res.status_code, res.text)

    def get_access_token(self, data: dict, headers: dict) -> str:
        res = requests.post('https://auth.worksmobile.com/oauth2/v2.0/token', data=data, headers=headers)
        if res.status_code != 200:
            self._handle_https_error(res.status_code, res.text)

        json_result = res.json()
        return json_result['access_token']

    @staticmethod
    def _handle_https_error(status_code: int, reason: str) -> None:
        if status_code == 503 or status_code == 500:
            # all 5xx errors are handled here
            raise ERROR_SERVER_FAILED(status_code=status_code, reason=reason)
        else:
            # all 4xx errors are handled here
            raise ERROR_CLIENT_REQUEST_FAILED(status_code=status_code, reason=reason)
