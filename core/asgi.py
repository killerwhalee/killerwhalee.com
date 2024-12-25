from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import os

from core import routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routes.websocket_urlpatterns))
        ),
    }
)
