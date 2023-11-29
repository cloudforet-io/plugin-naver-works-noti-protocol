import datetime
import jwt
from spaceone.core.manager import BaseManager
from plugin.connector.token_connector import TokenConnector


class TokenManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_jwt_token(self, client_id, service_account_id, private_key):
        payload = {
            "iss": client_id,
            "sub": service_account_id,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
        }
        encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')
        return encoded_jwt

    def create_access_token(self, client_id, client_secret, jwt_token):
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        params = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': jwt_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'bot bot.read bot.message',
        }
        token_connector = TokenConnector()
        access_token = token_connector.get_access_token(params, headers)
        return access_token

