import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
import time
import asyncio
class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        '''
        for i in range (0,10):
            si = str(i)
            obj = {'message':si}
            await asyncio.sleep(1)

            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(obj),
            })
        '''
        
    async def websocket_receive(self, event):
        print("receive", event)
        text_data_json = event['text']
        print(text_data_json)
        
        await self.send({
                'type': 'websocket.send',
                'text': text_data_json,
            })


    async def websocket_disconnect(self, event):
        print("disconnected", event)