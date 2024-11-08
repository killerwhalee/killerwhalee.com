from django.urls import re_path

from projects.interactive import consumer

app_name = "projects-interactive"

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumer.ChatConsumer.as_asgi()),
]
