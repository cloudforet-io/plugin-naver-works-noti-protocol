from spaceone.core.manager import BaseManager

NOTIFICATION_TYPE_MAP = {
    'INFO': '#43BEFF',
    'ERROR': '#FF6A6A',
    'SUCCESS': '#60B731',
    'WARNING': '#FFCE02',
    'DEFAULT': '#858895'
}

HEADER_ICON_URL = 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/spaceone-logo.png'


class MessageManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message = {
            "content": {
                "type": "flex",
                "altText": "This is a Flex Message",
                "contents": {
                    "type": "bubble",
                    "size": "giga",
                    "styles": {
                        "header": {},
                        "footer": {
                            "separator": True
                        }
                    }
                }
            }
        }

    @property
    def message(self) -> dict:
        return self._message

    def set_header_block(self, title: str, notification_type: str) -> None:
        self._message["content"]["contents"]["header"] = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                self._icon(HEADER_ICON_URL),
                self._title(title, notification_type)
            ]
        }

    def set_body_block(self, description: str, image_url: str, tags: list) -> None:
        body_data = {
            "type": "box",
            "layout": "vertical",
            "paddingBottom": "20px",
            "contents": []
        }
        if description:
            body_data["contents"].append(self._description(description))
        if image_url:
            body_data["contents"].append(self._image(image_url))
        if tags:
            body_data["contents"].append(self._tags(tags))
        self._message["content"]["contents"]["body"] = body_data

    def set_footer_block(self, link: str) -> None:
        footer_data = {
            "type": "box",
            "layout": "vertical",
            "separator": True,
            "contents": []
        }
        if link:
            footer_data["contents"].append(self._button(link))
        self._message["content"]["contents"]["footer"] = footer_data

    @staticmethod
    def _icon(icon_url: str) -> dict:
        return {
            "url": icon_url,
            "type": "image",
            "align": "end",
            "size": "sm",
            "aspectRatio": "6:1"
        }

    @staticmethod
    def _title(title: str, notification_type: str) -> dict:
        return {
            "layout": "horizontal",
            "type": "box",
            "separator": True,
            "spacing": "lg",
            "paddingBottom": "1px",
            "contents": [
                {
                    "layout": "vertical",
                    "type": "box",
                    "contents": [
                        {
                            "layout": "horizontal",
                            "type": "box",
                            "contents": [
                                {
                                    "layout": "vertical",
                                    "type": "box",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "4px",
                                    "backgroundColor": NOTIFICATION_TYPE_MAP[notification_type],
                                    "flex": 1,
                                    "cornerRadius": "sm"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "flex": 0,
                    "width": "8px"
                },
                {
                    "text": title,
                    "type": "text",
                    "size": "lg",
                    "weight": "bold",
                    "color": "#232533",
                    "wrap": True
                }
            ]
        }

    @staticmethod
    def _description(description: str) -> dict:
        return {
            "layout": "horizontal",
            "type": "box",
            "spacing": "md",
            "contents": [
                {
                    "layout": "vertical",
                    "type": "box",
                    "flex": 1,
                    "contents": [
                        {
                            "type": "text",
                            "text": description,
                            "size": "sm",
                            "wrap": True,
                            "margin": "md",
                            "flex": 7,
                            "color": "#232533"
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def _image(image_url: str) -> dict:
        return {
            "layout": "vertical",
            "type": "box",
            "flex": 1,
            "paddingTop": "15px",
            "paddingBottom": "10px",
            "contents": [
                {
                    "url": image_url,
                    "type": "image",
                    "aspectMode": "fit",
                    "size": "full"
                }
            ]
        }

    @staticmethod
    def _tags(tags: list) -> dict:
        tags_data = {
            "layout": "vertical",
            "type": "box",
            "margin": "xxl",
            "borderColor": "#DCDCDC",
            "borderWidth": "1px",
            "contents": []
        }

        for idx in range(len(tags)):
            row_data = {
                "layout": "horizontal",
                "type": "box",
                "paddingBottom": "6px",
                "paddingTop": "6px",
                "paddingStart": "8px",
                "paddingEnd": "8px",
                "contents": []
            }
            if not (idx % 2):
                row_data["backgroundColor"] = "#F8F8FC"
            print(tags[idx])
            key_data = {
                "layout": "horizontal",
                "type": "box",
                "flex": 1,
                "contents": [
                    {
                        "type": "text",
                        "text": tags[idx]["key"],
                        "color": "#898995",
                        "size": "sm",
                        "align": "start"
                    }
                ]
            }
            value_data = {
                "layout": "horizontal",
                "type": "box",
                "flex": 2,
                "contents": [
                    {
                        "type": "text",
                        "text": tags[idx]["value"],

                        "align": "start",
                        "size": "sm",
                        "wrap": True,
                        "color": "#232533"
                    }
                ]
            }
            row_data['contents'].append(key_data)
            row_data['contents'].append(value_data)
            tags_data['contents'].append(row_data)
        return tags_data

    @staticmethod
    def _button(link: str) -> dict:
        return {
            "layout": "horizontal",
            "type": "box",
            "contents": [
                {
                    "type": "button",
                    "height": "sm",
                    "style": "link",
                    "color": "#6638B6",
                    "flex": 1,
                    "action": {
                        "type": "uri",
                        "label": "Show More",
                        "uri": link
                    }
                }
            ]
        }
