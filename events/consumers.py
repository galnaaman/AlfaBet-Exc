# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = f"event_{self.event_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # destroy message from client
    async def receive(self, text_data):
        pass

    async def event_message(self, event):
        # Handle the event message
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
