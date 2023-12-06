import logging
from dateutil.parser import parse
from spaceone.core.manager import BaseManager
from plugin.manager.message_manager import MessageManager
from plugin.connector.naver_works_connector import NaverWorksConnector
from plugin.manager.token_manager import TokenManager

_LOGGER = logging.getLogger("spaceone")


class NotificationManager(BaseManager):
    def dispatch(
        self,
        token_mgr: TokenManager,
        bot_id: str,
        channel_id: str,
        message: dict,
        notification_type: str,
    ) -> None:
        token = token_mgr.token
        message_manager = MessageManager()

        title = message["title"]
        description = message.get("description")
        image_url = message.get("image_url")
        tags = message.get("tags", [])
        self.parse_occurred_at(message, tags)

        message_manager.set_header_block(title, notification_type)

        message_manager.set_body_block(description, image_url, tags)

        if link := message.get("link"):
            message_manager.set_footer_block(link)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        naver_works_connector = NaverWorksConnector()
        naver_works_connector.send_message(
            bot_id, channel_id, message_manager.message, headers
        )

    @staticmethod
    def parse_occurred_at(message: dict, tags: list) -> None:
        if occurred_at := message.get("occurred_at"):
            occurred_dt = parse(occurred_at)
            tags.append(
                {
                    "key": "Date",
                    "value": occurred_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "options": None,
                }
            )
