import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from scrumboard.models import Message
from asgiref.sync import async_to_sync

from scrumboard.views import email


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        if 'type' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'typing',
                    'user': text_data_json['user']
                }
            )
            return

        message = text_data_json['message']
        timestamp = text_data_json['timestamp']
        to_user = text_data_json['to_user']
        from_user = text_data_json['from_user']

        print('Message: ', message)
        print('Timestamp: ', timestamp)
        print('To user: ', to_user)
        print('From user: ', from_user)

        message_object = ''
        if message != '':
            message_object = Message.objects.create(
                value=message, date=timestamp, to_user=to_user, from_user=from_user
            )

        if message_object != '':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_object.toJSON(),
                }
            )

    def chat_message(self, event):
        message = event['message']
        loaded_message = json.loads(message)
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

        email(loaded_message['from_user'], loaded_message['value'], loaded_message['to_user'])

    def typing(self, event):
        self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user']
        }))
