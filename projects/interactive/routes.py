from django.urls import re_path

from projects.interactive import consumer

websocket_urlpatterns = [
    re_path(r"(?P<room_name>\w+)/$", consumer.ChatConsumer.as_asgi()),
]
