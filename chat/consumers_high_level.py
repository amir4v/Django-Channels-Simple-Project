import json
import os

from django.core import serializers
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer

from messenger.models import Message

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class AWC(AsyncWebsocketConsumer):
    async def connect(self):
        self.section_name = self.scope["url_route"]["kwargs"]["section_name"]
        self.room_group_name = "group_%s" % self.section_name

        # Join room group
        # group_name is/means general and channel_name is for you, your channel, your communication channel
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    #
    # these methods below are actions/methods/functions/we-send-with-them-specifically-in-their-own-way
    #
    
    # Receive message from room group
    async def send_message(self, event):
        messages = event["messages"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"messages": messages}))