from django.urls import re_path

from projects.interactive import consumer

app_name = "interactive"

websocket_urlpatterns = [
    re_path(
        r"ws/projects/interactive/(?P<room_name>\w+)/$",
        consumer.ChatConsumer.as_asgi(),
    ),
]
