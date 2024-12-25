from django.urls import path

from channels.routing import URLRouter

from projects import routes

websocket_urlpatterns = [
    path("ws/projects/", URLRouter(routes.websocket_urlpatterns)),
]
