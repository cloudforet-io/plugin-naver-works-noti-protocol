from plugin.connector.naver_works_connector import NaverWorksConnector
from spaceone.core.manager import BaseManager
from ..conf.naver_works_conf import *


def create_message_header(title, notification_type):
    header_dict = {
        "type": "box",
        "layout": "vertical",
        "contents": []
    }

    icon_dict = {
        "url": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/spaceone-logo.png",
        "type": "image",
        "align": "end",
        "size": "sm",
        "aspectRatio": "6:1"
    }

    title_dict = {
        "layout": "horizontal",
        "type": "box",
        "separator": True,
        "spacing": "lg",
        "paddingBottom": "8px",
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
                                "backgroundColor": NAVER_WORKS_CONF.attachment_color_map[notification_type],
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

    header_dict['contents'].append(icon_dict)
    header_dict['contents'].append(title_dict)

    return header_dict


def create_message_hero(image_url):
    hero_dict = {
        "layout": "vertical",
        "type": "box",
        "flex": 1,
        "contents": []
    }

    image_dict = {
        "url": image_url,
        "type": "image",
        "aspectMode": "fit",
        "size": "full",
        "aspectRatio": "2:1"
    }

    hero_dict['contents'].append(image_dict)

    return hero_dict


def create_body_table(tags):
    '''
    tags 의 options부분에 대해..? -> short value가 true 이거나 false일때 처리방식..? 에 대해 종민님께 여쭤보기
    '''

    table_dict = {
        "layout": "vertical",
        "type": "box",
        "margin": "xxl",
        "contents": []
    }

    for i in range(len(tags)):
        table_row_dict = {
            "layout": "horizontal",
            "type": "box",
            "paddingBottom": "6px",
            "paddingTop": "6px",
            "paddingStart": "8px",
            "paddingEnd": "8px",
            "contents": []
        }
        if not (i % 2):
            table_row_dict["backgroundColor"] = "#F8F8FC"

        key_dict = {
            "layout": "horizontal",
            "type": "box",
            "flex": 1,
            "contents": [
                {
                    "type": "text",
                    "text": tags[i]['key'],
                    "color": "#898995",
                    "size": "sm",
                    "align": "start"
                }
            ]
        }
        value_dict = {
            "layout": "horizontal",
            "type": "box",
            "flex": 2,
            "contents": [
                {
                    "type": "text",
                    "text": tags[i]['value'],
                    "align": "start",
                    "size": "sm",
                    "wrap": True,
                    "color": "#232533"
                }
            ]
        }
        table_row_dict['contents'].append(key_dict)
        table_row_dict['contents'].append(value_dict)
        table_dict['contents'].append(table_row_dict)

    return table_dict


def create_message_body(description, tags):
    body_dict = {
        "type": "box",
        "layout": "vertical",
        "paddingBottom": "20px",
        "contents": []
    }

    text_dict = {
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
    body_dict['contents'].append(text_dict)

    table_dict = create_body_table(tags)
    body_dict['contents'].append(table_dict)

    return body_dict


def create_message_footer(link):
    footer_dict = {
        "layout": "vertical",
        "type": "box",
        "separator": True,
        "contents": []
    }

    button_dict = {
        "layout": "horizontal",
        "type": "box",
        "contents": []
    }
    link_dict = {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#6638B6",
        "flex": 1,
        "action": {
            "type": "uri",
            "label": "More...",
            "uri": link
        }
    }
    button_dict['contents'].append(link_dict)
    footer_dict['contents'].append(button_dict)

    return footer_dict


class NaverWorksManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, bot_id, channel_id, access_token, message, notification_type):
        title = message.get('title', '')
        message_header = create_message_header(title, notification_type)

        image_url = message.get('image_url', '')
        message_hero = None
        if image_url:
            message_hero = create_message_hero(image_url)

        tags = message.get('tags', [])
        description = message.get('description', '')
        message_body = create_message_body(description, tags)

        # callbacks = message.get('callbacks', [])
        link = message.get('link', '')
        message_footer = create_message_footer(link)

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        params = {
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
                    },
                    "header": message_header,
                    "body": message_body,
                    "footer": message_footer
                }
            }
        }
        naver_works_connector = NaverWorksConnector()
        naver_works_connector.send_message(bot_id, channel_id, params, headers)
