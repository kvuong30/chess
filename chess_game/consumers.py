import json
import chess
import chess.engine
from channels.generic.websocket import AsyncWebsocketConsumer
from .db_util import games_collection

class ChessGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chess_game_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.accept()

        # Initialize a new chess game or resume an existing game
        self.board = chess.Board()
        self.game_data = games_collection.find_one({"room_name": self.room_name})

        if self.game_data:
            self.board.set_fen(self.game_data['fen'])

        # Send initial game state to WebSocket
        await self.send_game_state()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        move = text_data_json['move']

        # Apply the move to the board
        try:
            self.board.push_san(move)
        except ValueError as e:
            print(f"Invalid move: {move}")
            return

        # Save the game state in MongoDB
        games_collection.update_one(
            {"room_name": self.room_name},
            {"$set": {"fen": self.board.fen()}},
            upsert=True
        )

        # Send updated game state to WebSocket
        await self.send_game_state()

        # Let the bot make its move if it's the bot's turn
        if self.board.turn == chess.BLACK:
            await self.bot_move()

    async def send_game_state(self):
        game_state = {
            'fen': self.board.fen(),  # Send FEN to update the board
            'turn': 'Black' if self.board.turn == chess.BLACK else 'White'
        }
        await self.send(text_data=json.dumps(game_state))

    async def bot_move(self):
        # Make a move for the bot using python-chess engine
        # TODO
        with chess.engine.SimpleEngine.popen_uci("/path/to/your/chess/engine") as engine:
            result = engine.play(self.board, chess.engine.Limit(time=2.0))
            self.board.push(result.move)
            games_collection.update_one(
                {"room_name": self.room_name},
                {"$set": {"fen": self.board.fen()}},
                upsert=True
            )
            # Send the updated game state to the WebSocket
            await self.send_game_state()
