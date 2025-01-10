## MongoDB and Django

### Overview: Chess App with Django, MongoDB, and AI Bot

Many developers are strategic thinkers and enjoy strategic games, such as chess. Some developers are even avid chess players, who would take the time to analyze their moves and learn from their mistakes, similar to the problem-solving and strategic learning/planning of coding. Ultimately, both coding and chess can be intellectually rewarding and involve a mix of logic and creativity, as top chess players often think "outside the box," creating new opening variations, tactical combinations, or endgame strategies.

This tutorial aims to implement the beautiful game of chess as a web application with Django as the backend, MongoDB for the database, and an AI chess bot that users can play against.


### 1. Setting Up the Project Environment
#### 1.1 Install Dependencies

* **Python 3.7+**
* **Django**: Open-source web framework
* **MongoDB**: NoSQL database to store game data (using ```pymongo``` to integrate MongoDB with Django)
* **Python packages**:
  * django
  * djangorestframework
  * pymongo
  * django-cors-headers (for handling CORS)
  * chess (Python chess library)

First, set up a virtual environment and install necessary dependencies, run the following commands:
```bash
# create and activate a virtual environment
python3 -m venv chess_game_env
source chess_game_env/bin/activate  # for Linux/macOS
# or
chess_game_env\Scripts\activate  # for Windows

# install required packages
pip install django djangorestframework pymongo django-cors-headers chess
```

### 2. Create Django Project
#### 2.1. Set Up Django Project

Start by creating a new Django project and app:

```bash
django-admin startproject chess_game
cd chess_game
django-admin startapp game
```

#### 2.2. Set Up MongoDB Database in Django

Ensure you have MongoDB installed and running on your machine, see more details: https://www.mongodb.com/docs/manual/installation/.

For example, to install/start MongoDB on macOS:

(Reference: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
```bash
brew update
brew upgrade
brew tap mongodb/brew
brew install mongodb-community@8.0 # or any mongodb version you prefer
brew services start mongodb/brew/mongodb-community
brew services list
mongod --version # once installed, show the mongoDB version
```

In ```chess_game/settings.py```, add the following changes:

```python
INSTALLED_APPS = [
    ...,
    'corsheaders',
    'rest_framework',
    'game',
]

MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'game/templates'],  # Add the templates folder of your app
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# MongoDB connection settings (will be handled in views.py with PyMongo)
DATABASES = {}
```


### 3. Design Models for Chess Game

In ```game/models.py```, we will define a model to store the state of the chess game. This will include the position of each piece and the current turn.

```python
from django.db import models


class ChessGame(models.Model):
    game_id = models.CharField(max_length=32, unique=True)
    board_state = models.JSONField(default=dict)  # Store positions of all pieces
    turn = models.CharField(max_length=5, default='white')  # 'white' or 'black'

    def __str__(self):
        return f"Game {self.game_id}, Turn: {self.turn}"

```
The ```board_state``` is stored as a JSON field, where the state of each piece (e.g., 'P' for pawn, 'R' for rook) and its position (e.g., 'a1', 'h8') will be saved.

### 3.1. Create the API Views
We will use Django REST framework to expose API endpoints for interacting with the game.

In ```game/views.py```:

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import chess

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.chessgame_db  # database name
games_collection = db.games  # Collection for storing chess game state


# Initialize a new chess game
def initialize_game():
    board = chess.Board()
    game_state = {
        'board_state': board.fen(),  # Store the FEN representation of the board
        'turn': 'white',  # Start with white's turn
    }
    return game_state


# View to start a new game
@csrf_exempt
def start_game(request):
    game_id = 'game123'  # Static game ID for now (could be dynamic)
    game_state = initialize_game()

    # Store the initial game state in MongoDB
    games_collection.insert_one({
        'game_id': game_id,
        'board_state': game_state['board_state'],
        'turn': game_state['turn']
    })

    return JsonResponse({
        'game_id': game_id,
        'board_state': game_state['board_state'],
        'turn': game_state['turn']
    })


# View to get the current state of the game
def get_game_state(request, game_id):
    game = games_collection.find_one({'game_id': game_id})
    if game:
        return JsonResponse({
            'board_state': game['board_state'],
            'turn': game['turn']
        })
    else:
        return JsonResponse({'error': 'Game not found'}, status=404)


# View to make a move
@csrf_exempt
def make_move(request, game_id):
    move = request.POST.get('move')  # Move in UCI format (e.g., 'e2e4')

    game = games_collection.find_one({'game_id': game_id})
    if not game:
        return JsonResponse({'error': 'Game not found'}, status=404)

    board = chess.Board(game['board_state'])

    # Validate the move
    if board.is_legal(chess.Move.from_uci(move)):
        board.push(chess.Move.from_uci(move))  # Apply the move
        new_game_state = {
            'board_state': board.fen(),
            'turn': 'black' if game['turn'] == 'white' else 'white'
        }

        # Update game state in MongoDB
        games_collection.update_one({'game_id': game_id}, {'$set': new_game_state})

        return JsonResponse({
            'board_state': new_game_state['board_state'],
            'turn': new_game_state['turn']
        })
    else:
        return JsonResponse({'error': 'Illegal move'}, status=400)

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

```


### 3.2. Create the Serializers
In ```game/serializers.py```, we need to create a serializer for the ```ChessGame``` model:
```python
from rest_framework import serializers
from .models import ChessGame


class ChessGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessGame
        fields = ['game_id', 'board_state', 'turn']

```


### 4. Define URLs for the views:

Add ```game/urls.py``` to map the views to URLs:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Route for the index page
    path('api/games/start/', views.start_game, name='start_game'),  # Ensure this path exists
    path('api/games/<str:game_id>/get_game_state/', views.get_game_state, name='get_game_state'),
    path('api/games/<str:game_id>/make_move/', views.make_move, name='make_move'),
]
```
Also, add ```game.urls``` to the main ```chess_game/urls.py```:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
]
```

#### 5.2. Templates for the Board

Create a template ```game/templates/index.html``` to render the chessboard and move history.
```bash
mkdir -p game/templates
```


Add the following HTML to ```game/templates/index.html```:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chess Game</title>
  <style>
    table {
      border-collapse: collapse;
      margin: 50px;
    }
    td {
      width: 50px;
      height: 50px;
      text-align: center;
      vertical-align: middle;
      border: 1px solid #000;
    }
    .light {
      background-color: #f0d9b5;
    }
    .dark {
      background-color: #b58863;
    }
    .piece {
      font-size: 36px;
    }
  </style>
</head>
<body>
  <h1>Chess Game</h1>
  <div id="board"></div>
  <button id="startBtn">Start New Game</button>

  <script>
    const boardElement = document.getElementById("board");
    const startBtn = document.getElementById("startBtn");
    let gameId = 'game123';  // Fixed game ID
    let boardState = null;

    // Render the chessboard
    function renderBoard(boardState) {
      let boardHtml = '<table>';
      const rows = boardState.split(' ')[0].split('/');
      let rowNum = 8;

      rows.forEach(row => {
        boardHtml += '<tr>';
        let colNum = 1;
        for (let char of row) {
          if (parseInt(char)) {
            // Empty spaces
            for (let i = 0; i < parseInt(char); i++) {
              boardHtml += `<td class="${(rowNum + colNum) % 2 === 0 ? 'light' : 'dark'}"></td>`;
              colNum++;
            }
          } else {
            // Chess piece
            const piece = char.toUpperCase();
            boardHtml += `<td class="${(rowNum + colNum) % 2 === 0 ? 'light' : 'dark'}"><span class="piece">${piece}</span></td>`;
            colNum++;
          }
        }
        boardHtml += '</tr>';
        rowNum--;
      });

      boardHtml += '</table>';
      boardElement.innerHTML = boardHtml;
    }

    // Fetch the initial game state
    function startNewGame() {
      fetch('http://localhost:8000/api/games/start/', {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        boardState = data.board_state;
        renderBoard(boardState);
      });
    }

    // Start a new game when the button is clicked
    startBtn.addEventListener("click", startNewGame);

    // Initialize game on page load
    window.onload = () => {
      startNewGame();
    };
  </script>
</body>
</html>
```


### 6. Run the Development Server
Since we're using MongoDB directly with ```PyMongo```, no migrations are needed. You can now run the Django server:

```bash
python manage.py runserver
```

### 7. View chess game
Open in your browser: http://localhost:8000/
