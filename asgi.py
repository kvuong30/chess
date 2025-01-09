import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from chess_game import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chess_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^ws/chess/(?P<roomName>\w+)/$", consumers.ChessGameConsumer.as_asgi()),
        ])
    ),
})
