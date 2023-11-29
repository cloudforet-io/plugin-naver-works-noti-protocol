import requests
from spaceone.core.connector import BaseConnector


class NaverWorksConnector(BaseConnector):

    def send_message(self, bot_id, channel_id, params, headers):
        r = requests.post(f'https://www.worksapis.com/v1.0/bots/{bot_id}/channels/{channel_id}/messages', data=params,
                          headers=headers)
