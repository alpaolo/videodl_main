import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer

import time

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_name = 'youtube'
        print("room", self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        print("group", self.room_group_name)
        # Join room group
        
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("message received from web socket: ", message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'socket_message',
                'message': message
            }
        )

    # Receive message from room group
    # Questo è l'handler del tipo di messaggio
    def socket_message(self, event):
        message = event['message']
        print("message received from room group: ", message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # Send a message
    def send_message(self, message):
        self.send(text_data=json.dumps({
            'message': message
        }))


    def get_me(self):
        return self