# chess_game/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chess.consumers import ChessConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chess_game.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Define WebSocket URL for the chess game
            path("ws/game/<str:game_id>/", ChessConsumer.as_asgi()),
        ])
    ),
})
