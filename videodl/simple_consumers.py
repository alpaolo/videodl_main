from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class SimpleConsumer(WebsocketConsumer):

    def __init__(self):
        super().__init__() 


    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept',
        })
        self.accept()

    def websocket_receive(self, event):
        data = json.loads(event['text'])
        print("Ricevuto in websocket: " + data['message'])
        self.send(
            {
                'type': 'custom.type',
                'message': data['message']
            }
        )


    def custom_type(self, event):
        print ( " Ricevuto messaggio custom_type")


    def websocket_send(self, event):
        self.send({
            'type': 'websocket.receive',
            'text': event['text'],
        })


    def websocket_disconnect(self, event):
        self.close()