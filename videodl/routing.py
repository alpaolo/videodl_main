# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/downlad/rai/(?P<action>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/download/youtube/(?P<action>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

