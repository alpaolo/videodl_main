import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . asyncprocess import AsyncProcess
import asyncio

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['comm_name']
        print ("CONNESSIONE ATTIVA: ",self.scope)
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
        # Comunico al client l'avvenuto start del processo e la progressione dello stesso
        self.send(text_data=json.dumps({
            'message': 'progress_download'
        }))
        process.download_process(dlurl)
       

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
                'type': 'client_message',
                'message': message
            }
        )

    # Receive message from room group
    # Handler per il tipo "client_message"
    # Trasmette il messahggio al client
    def client_message(self, event):
        message = event['message']
        print ( "CLIENT: ho ricevuto il messagio nell'handler del client", message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    