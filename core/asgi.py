from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import projects.interactive

import os

import projects.interactive.routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(projects.interactive.routes.websocket_urlpatterns))
        ),
    }
)
