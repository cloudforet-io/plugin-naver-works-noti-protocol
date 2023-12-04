from typing import Union
from pydantic import BaseModel

__all__ = ['ChannelData']


class ChannelData(BaseModel):
    channel_id: str
    bot_id: str
    client_id: str
    client_secret: str
    service_account_id: str
    private_key: str
