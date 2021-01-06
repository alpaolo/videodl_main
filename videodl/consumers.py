import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . asyncprocess import AsyncProcess
import asyncio

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print ("socket_connected")
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # Riceve il messaggio generico dal socket che viene intercettato dall'handler relativo al tipo di messaggio
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        print ( "RECEIVE: ho ricevuto il messagio: ", message, " e lo indirizzo all'handler: ", type)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': type,
                'message': message
            }
        )

        
    # Handler per il tipo "start_download"    
    def start_download(self, event):
        message = event['message']
        dlurl = message
        type = event['type']
        print ( "START DOWNLOAD: ho ricevuto il messagio di: ", type , "con messaggio: " , message, " e inizio la procedura di download" )
        process = AsyncProcess(self)
        #process.sendmessage()
        process.download_process(dlurl)

        '''
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'end_download',
                'message': message
            }
        )
        '''

     # Handler per il tipo "progress_download"    
    def progress_download(self, event):
        message = event['message']
        type = event['type']
        print ( "PROGRESS DOWNLOAD: ho ricevuto il messagio di: ", type , "con messaggio: " , message)
        


    # Handler per il tipo "end_download"    
    def end_download(self, event):
        message = event['message']
        type = event['type']
        print ( "END DOWNLOAD: ho ricevuto il messagio di: ", type , "con messaggio: " , message)
        # Ricevuto il segnale di fine download lo inoltro al client
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    # Handler per il tipo "chat_message"
    def chat_message(self, event):
        message = event['message']
        print ( "CHAT MESSAGE: ho ricevuto il messagio in chat", message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    