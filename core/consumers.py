import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AbstractCommentConsumer:
    """
    Сlass to describe functionality for sending a message
    and clearing a connection about group in redis
    """
    async def send_comment(self, event):
        message = event['message']
        event_type = event['event_type']
        await self.send(text_data=json.dumps({
            'type': event_type,
            'message': message
        }))

    async def disconnect(self, close_code):
        await self.chann8el_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


class MainPageCommentConsumer(AsyncWebsocketConsumer, AbstractCommentConsumer):
    """
    Ws handler for main_page connections for receiving top level comments
    """
    async def connect(self):
        self.room_group_name = 'main_comments'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


class ChildCommentsConsumer(AsyncWebsocketConsumer, AbstractCommentConsumer):
    """
    Ws handler for main_page connections for receiving child comments
    """
    async def connect(self):
        comment_id = self.scope['url_route']['kwargs']['id']

        self.room_group_name = f"child_comments_{comment_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

