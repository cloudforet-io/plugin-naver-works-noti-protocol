from spaceone.core.manager import BaseManager


class ProtocolManager(BaseManager):

    def get_metadata(self) -> dict:
        return {
            "metadata": {
                "data_type": "SECRET",
                "data": {
                    "schema": self._get_json_schema()
                }
            }
        }

    @staticmethod
    def _get_json_schema() -> dict:
        return {
            "properties": {
                "client_id": {
                    "description": "id for the client app created on Naver Works Developer Console",
                    "minLength": 20,
                    "title": "Client ID",
                    "type": "string",
                    "examples": ["xF4Wd4TJdxc23vjabc23"]
                },
                "client_secret": {
                    "description": "secret for the client app",
                    "minLength": 10,
                    "title": "Client Secret",
                    "type": "string",
                    "examples": ["ffd23sdv3b"]
                },
                "service_account": {
                    "description": "service account associated with the client app",
                    "minLength": 22,
                    "title": "Service Account",
                    "type": "string",
                    "examples": ["examp.serviceaccount@example"]
                },
                "bot_id": {
                    "description": "id for the message bot created on Naver Works Developer Console",
                    "minLength": 7,
                    "title": "Message Bot ID",
                    "type": "string",
                    "examples": ["6942032"]
                },
                "channel_id": {
                    "description": "id for the channel(group chat room)",
                    "minLength": 36,
                    "title": "Channel ID",
                    "type": "string",
                    "examples": ["d41f1039-1215-5952-88d6-2d5339cddfcb"]
                },
                "private_key": {
                    "description": "private key associated with the client app",
                    "minLength": 1000,
                    "title": "Private Key",
                    "type": "textarea",
                    "examples": ["----BEGIN PRIVATE KEY---— .... ----END PRIVATE KEY---—"]
                },
            },
            "required": ["client_id", "client_secret", "service_account", "bot_id", "channel_id",
                         "private_key"],
            "type": "object"
        }
