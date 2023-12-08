import datetime
import jwt
import logging
from spaceone.core.manager import BaseManager
from plugin.connector.naver_works_connector import NaverWorksConnector

_LOGGER = logging.getLogger("spaceone")


class TokenManager(BaseManager):
    def __init__(
        self, *args, client_id, client_secret, service_account, private_key, **kwargs
    ):
        super().__init__(*args, **kwargs)
        _jwt = self._create_jwt_token(client_id, service_account, private_key)
        self._token = self._create_access_token(client_id, client_secret, _jwt)

    @property
    def token(self):
        return self._token

    @staticmethod
    def _create_jwt_token(
        client_id: str, service_account: str, private_key: str
    ) -> str:
        payload = {
            "iss": client_id,
            "sub": service_account,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
        }

        return jwt.encode(payload, private_key, algorithm="RS256")

    @staticmethod
    def _create_access_token(client_id: str, client_secret: str, jwt_token: str) -> str:
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        params = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "bot bot.read bot.message",
        }
        naver_works_connector = NaverWorksConnector()
        return naver_works_connector.get_access_token(params, headers)
