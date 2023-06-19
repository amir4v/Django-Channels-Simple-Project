import json

from django.core import serializers
from django.contrib.auth.models import User

from messenger.models import Message
from .consumers_high_level import AWC


class ChatConsumer(AWC):
    async def receive(self, text_data):
        """
        inja bayad az text_data yek route begirim ke chikar mikhad bokone va shayad yek status.
        
        """
        
        text_data_json = json.loads(text_data)
        message = text_data_json["messages"]
        
        if message == 'load':
            objects = serializers.serialize('json', Message.objects.all(), fields=('id', 'From', 'to', 'text'))
        else:
            objects = serializers.serialize(
                'json',
                [Message.objects.create(From=User(id=1), to=User(id=1), text=message)],
                fields=('id', 'From', 'to', 'text')
            )
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_message", "messages": objects}
        )