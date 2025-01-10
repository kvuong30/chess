# chess/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient
from chess import Board  # Python chess library for AI and game logic
import chess.engine

class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = f"chess_{self.game_id}"

        # Accept the WebSocket connection
        await self.accept()

        # Create MongoDB connection
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['chess_db']
        self.games_collection = self.db['games']

        # Check if the game exists, otherwise create a new game
        game = self.games_collection.find_one({'game_id': self.game_id})
        if not game:
            self.games_collection.insert_one({
                'game_id': self.game_id,
                'board': Board().fen(),  # Start with a fresh chess board
                'turn': 'white',
                'player_white': None,
                'player_black': None,
                'history': []
            })
            game = self.games_collection.find_one({'game_id': self.game_id})

        self.game_state = game

    async def disconnect(self, close_code):
        # Handle disconnection if needed
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']

        if action == 'move':
            move = data['move']
            await self.make_move(move)

        # Broadcast the updated game state to all connected clients
        await self.send(text_data=json.dumps({
            'game_state': self.game_state,
        }))

    async def make_move(self, move):
        # Apply the player's move and update the board
        board = chess.Board(self.game_state['board'])
        board.push_san(move)

        # Now let the AI make its move
        with chess.engine.SimpleEngine.popen_uci("/path/to/stockfish") as engine:
            ai_move = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(ai_move.move)
            # Log AI move to check if it's working
            print(f"----> AI move: {ai_move.move}")

        self.game_state['board'] = board.fen()
        self.game_state['turn'] = 'white'  # Player's turn after AI's move

        # Save the game state to MongoDB
        self.games_collection.update_one(
            {'game_id': self.game_id},
            {'$set': {'board': board.fen(), 'turn': self.game_state['turn']}}
        )

