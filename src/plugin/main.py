import logging
from spaceone.core.service import check_required
from spaceone.notification.plugin.protocol.lib.server import ProtocolPluginServer
from plugin.manager.token_manager import TokenManager
from plugin.manager.notification_manager import NotificationManager
from plugin.manager.protocol_manager import ProtocolManager
from plugin.model.channel_data import ChannelData

app = ProtocolPluginServer()

_LOGGER = logging.getLogger("spaceone")


@app.route("Protocol.init")
def protocol_init(params: dict) -> dict:
    """init plugin by options

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
    protocol_manager = ProtocolManager()
    return protocol_manager.get_metadata()


@app.route("Protocol.verify")
def protocol_verify(params: dict) -> None:
    """Verifying protocol plugin

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


@app.route("Notification.dispatch")
def notification_dispatch(params: dict):
    """dispatch notification

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

    channel_data = ChannelData(**params["channel_data"])
    message = params["message"]
    notification_type = params["notification_type"]

    notification_manager = NotificationManager()

    token_mgr = TokenManager(
        client_id=channel_data.client_id,
        client_secret=channel_data.client_secret,
        service_account=channel_data.service_account,
        private_key=channel_data.private_key,
    )
    notification_manager.dispatch(
        token_mgr,
        channel_data.bot_id,
        channel_data.channel_id,
        message,
        notification_type,
    )
