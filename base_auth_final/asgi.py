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
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
            video_call.routing.websocket_urlpatterns +
            createTeams.routing.websocket_urlpatterns
        )
    ),
    ),
})


# import os
# import django
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE","base_auth_final.settings")
# django.setup()
# application = get_default_application()
