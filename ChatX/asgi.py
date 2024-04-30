"""
ASGI config for ChatX project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chatApp.middleware.channel_middleware import JWTWebSocketMiddleware
from chatApp.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatX.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": JWTWebSocketMiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))
})