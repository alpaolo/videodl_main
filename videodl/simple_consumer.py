from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
import json

class SimpleConsumer(SyncConsumer):

    def __init__(self):
        super().__init__() 


    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept',
        })

    def websocket_receive(self, event):
        data = json.loads(event['text'])
        print(data['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    def websocket_send(self, event):
        
        self.send({
            'type': 'websocket.receive',
            'text': event['text'],
        })


    def websocket_disconnect(self, event):
        self.close()