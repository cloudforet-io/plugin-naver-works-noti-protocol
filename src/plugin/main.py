from spaceone.core.error import ERROR_REQUIRED_PARAMETER
from spaceone.core.service import check_required
from spaceone.notification.plugin.protocol.lib.server import ProtocolPluginServer
from plugin.manager.naver_works_manager import NaverWorksManager
from plugin.manager.token_manager import TokenManager

app = ProtocolPluginServer()


@app.route('Protocol.init')
def protocol_init(params: dict) -> dict:
    """ init plugin by options

    Args:
        params (ProtocolInitRequest): {
            'options': 'dict',    # Required
            'domain_id': 'str'
        }

    Returns:
        PluginResponse: {
            'metadata': 'dict'
        }
    """
    print("HERE?")
    return {"metadata": {"options_schema": _create_options_schema()}}


@app.route('Protocol.verify')
def protocol_verify(params: dict) -> None:
    """ Verifying protocol plugin

    Args:
        params (ProtocolVerifyRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'domain_id': 'str'
        }

    Returns:
        None
    """
    pass


@app.route('Notification.dispatch')
@check_required(['options', 'secret_data', 'channel_data', 'message', 'notification_type'])
def notification_dispatch(params: dict) -> dict:
    """ dispatch notification

    Args:
        params (NotificationDispatchRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'channel_data': 'dict', # Required
            'message': 'dict',
            'notification_type': 'str',
        }

    Returns:
        None
    """
    channel_data = params.get('channel_data')
    validate_channel_data(channel_data)
    channel_id = params['channel_data'].get('channel_id', '')
    bot_id = params['channel_data'].get('bot_id', '')
    client_id = params['channel_data'].get('client_id', '')
    client_secret = params['channel_data'].get('client_secret', '')
    service_account_id = params['channel_data'].get('service_account_id', '')
    private_key = params['channel_data'].get('private_key', '')

    message = params['message']
    notification_type = params['notification_type']
    validate_message(message)
    validate_notification_type(notification_type)

    token_manager = TokenManager()
    naver_works_manager = NaverWorksManager()

    jwt_token = token_manager.create_jwt_token(client_id, service_account_id, private_key)
    access_token = token_manager.create_access_token(client_id, client_secret, jwt_token)

    naver_works_manager.dispatch(bot_id, channel_id, access_token, message, notification_type)


def validate_channel_data(channel_data):
    if 'channel_id' not in channel_data:
        raise ERROR_REQUIRED_PARAMETER(key='channel_data.channel_id')

    if 'private_key' not in channel_data:
        raise ERROR_REQUIRED_PARAMETER(key='channel_data.private_key')

    if 'client_id' not in channel_data:
        raise ERROR_REQUIRED_PARAMETER(key='channel_data.client_id')

    if 'client_secret' not in channel_data:
        raise ERROR_REQUIRED_PARAMETER(key='channel_data.client_secret')

    if 'service_account_id' not in channel_data:
        raise ERROR_REQUIRED_PARAMETER(key='channel_data.service_account_id')

    if 'bot_id' not in channel_data:
        raise ERROR_REQUIRED_PARAMETER(key='channel_data.bot_id')


def validate_message(message):
    title = message.get('title', '')
    if title:
        if not isinstance(title, str):
            raise ValueError(f'Title input is supposed to be a string type! Your input is {title}.')

    callbacks = message.get('callbacks', '')
    if callbacks:
        if not isinstance(callbacks, list):
            raise ValueError(f'Callbacks input is supposed to be a list type! Your input is {callbacks}.')


def validate_notification_type(notification_type):
    if notification_type not in ['INFO', 'ERROR', 'SUCCESS', 'WARNING']:
        raise ValueError(
            f'Notification type is supposed to be one of the following: INFO, ERROR, SUCCESS, WARNING. Your input is {notification_type}.')


def _create_options_schema():
    return {
        "data_type": "SECRET",
        "data": {
            "schema": {
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
                    "secret_key": {
                        "description": "private key associated with the client app",
                        "minLength": 1000,
                        "title": "Private Key",
                        "type": "textarea",
                        "examples": ["----BEGIN PRIVATE KEY---— .... ----END PRIVATE KEY---—"]
                    },
                },
                "required": ["client_id", "client_secret", "service_account", "bot_id", "channel_id",
                             "secret_key"],
                "type": "object"
            }
        }
    }
