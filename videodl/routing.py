# chat/routing.py
from django.urls import re_path

from . import simple_consumers
#from . import async_consumers
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/downlad/rai/(?P<action>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/download/youtube/(?P<action>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/download/youtube/', consumers.ChatConsumer.as_asgi()),
]

'''
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', async_consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/downlad/rai/(?P<action>\w+)/$', async_consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/download/youtube/(?P<action>\w+)/$', async_consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/download/youtube/', async_consumers.ChatConsumer.as_asgi()),
]


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', simple_consumers.SimpleConsumer.as_asgi()),
    re_path(r'ws/downlad/rai/(?P<action>\w+)/$', simple_consumers.SimpleConsumer.as_asgi()),
    re_path(r'ws/download/youtube/(?P<action>\w+)/$', simple_consumers.SimpleConsumer.as_asgi()),
    re_path(r'ws/download/youtube/', simple_consumers.SimpleConsumer.as_asgi()),
]
'''