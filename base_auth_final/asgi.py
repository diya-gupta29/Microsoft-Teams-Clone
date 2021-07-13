"""
ASGI config for base_auth_final project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import video_call.routing
import createTeams.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base_auth_final.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
            video_call.routing.websocket_urlpatterns +
            createTeams.routing.websocket_urlpatterns
        )
    ),
    ),
})
