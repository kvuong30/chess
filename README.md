## MongoDB and Django

### Overview - Game of Codes: Crafting a Chess App with Django and MongoDB

Building a chess app is not just about writing code—it's also a strategy. Just like in chess, programming requires careful thought, planning, and a systematic approach. In chess, each move builds upon the last, much like how software development requires breaking down complex problems into smaller, manageable pieces. Each piece on the chessboard has a distinct role, just like each function or class in programming serves a specific purpose. Whether you're developing a chess app or playing a game of chess, the key to success lies in foresight, creativity, and the ability to adapt to new situations. Programming with Django and MongoDB will be like strategizing on a chessboard, where you create a structure, anticipate moves, and ensure every part of the app works together harmoniously. Many developers are strategic thinkers and enjoy strategic games, such as chess. Some developers are even avid chess players, who would take the time to analyze their moves and learn from their mistakes, similar to the problem-solving and strategic learning/planning of programming. Ultimately, both coding and chess can be intellectually rewarding and involve a mix of logic and creativity, as top chess players often think "outside the box," creating new opening variations, tactical combinations, or endgame strategies.

This tutorial aims to serve as a starting point in implementing the beautiful game of chess as a web application with Django as the backend, MongoDB for the database, and an AI chess bot that users can play against. It’ll guide you through creating a fully functional chess app using Django for the backend and MongoDB for the database. By the end of the tutorial, you will have a web application where users can play chess games, see their current game state, and even retrieve past game data. We’ll use Django for handling the backend logic, creating API endpoints, and managing user authentication. MongoDB, a NoSQL database, will store game states, player moves, and metadata in a way that’s flexible and scalable. We’ll break down each section of the app step by step, explaining how Django interacts with MongoDB, and how the front-end (which we'll keep simple) displays the current state of the chess game.

### Why Django and MongoDB?
In this tutorial, Django and MongoDB were chosen for several key reasons.

#### Why Django?
Django is a high-level Python web framework that promotes rapid development and clean, pragmatic design. It's known for its "batteries-included" philosophy, meaning it comes with many built-in features, such as authentication, routing, admin interfaces, and database models. This makes Django an excellent choice for developers who want to focus on building the app rather than reinventing the wheel.
While there are other Python frameworks like Flask that offer greater flexibility, Django’s comprehensive nature and its "convention over configuration" approach make it a better choice for building scalable applications quickly. Flask is lightweight and gives you more control over the individual components of your app, but this can become overwhelming as the app grows in complexity. Django’s built-in admin panel, form handling, and authentication system allow you to build a robust application without needing to configure these features from scratch. Additionally, Django’s structure makes it easier to scale the app as you introduce more features like player profiles, game history, and real-time multiplayer gameplay.

#### Why MongoDB?
MongoDB is a NoSQL database that stores data in JSON-like documents, which makes it highly flexible and scalable. It’s particularly useful when the data schema is dynamic or when you expect to store a lot of unstructured or semi-structured data. For our chess app, MongoDB is a perfect fit because the chessboard's state can change rapidly, and different games might have different amounts of metadata (like move history or player statistics). Relational databases like PostgreSQL or MySQL are great for structured data and complex relationships, but since we don't need complex joins in this app, MongoDB allows us to store the game state in a more flexible way using its native JSON format. For example, the  ```board_state``` in the ChessGame model is stored as a ```JSONField```, which is easy to manipulate and extend. This flexibility is ideal for a chess game where the data may need to change dynamically and quickly.

Together, Django and MongoDB provide a strong, flexible, and efficient stack for building a chess app. Django’s ease of use and built-in features make it an ideal choice for web development, while MongoDB’s flexibility enables us to store the game data in a way that allows for future enhancements, like adding more complex game features or expanding the data model to support other game modes. This combination ensures the app is scalable, maintainable, and easy to extend as your chess platform grows.

### 1. Setting Up the Project Environment
#### 1.1 Prerequisites: What You Need to Get Started
* **Python 3.7+**
* **Django**: Open-source web framework
* **MongoDB**: NoSQL database to store game data (using ```pymongo``` to integrate MongoDB with Django)
* **Python packages**:
  * django
  * djangorestframework
  * pymongo
  * django-cors-headers (for handling CORS)
  * chess (Python chess library)
  * channels_redis

#### 1.2 Create virtual environment

For a cleaner development experience and to avoid potential package version conflicts, it’s highly recommended to create a virtual environment for your Django project.  A virtual environment is an isolated workspace that allows you to manage project-specific dependencies without affecting your global Python installation. This is crucial for maintaining clean and consistent project environments, especially when working on multiple projects with different dependency versions. By using a virtual environment, you ensure that your project’s dependencies are neatly contained, preventing potential conflicts between different libraries or versions of Python.

If you’re new to virtual environments, see this official Python guide provides detailed instructions on how to create and manage virtual environments: https://docs.python.org/3/tutorial/venv.html

To create a virtual environment, follow these steps:

#### For Linux/macOS:
Create and activate a virtual environment in Linux/macOS:
```bash
python3 -m venv chess_game_env
source chess_game_env/bin/activate
```

#### For Windows:
Create and activate a virtual environment in Windows:
```bash
python3 -m venv chess_game_env
chess_game_env\Scripts\activate
```

#### 1.3 Install Dependencies

To install necessary dependencies, run the following commands:
```bash
# install required packages
pip install django djangorestframework pymongo django-cors-headers chess channels_redis
```

### 2. Create Django Project
#### 2.1. Set Up Django Project

Django is a powerful web framework that provides a structured approach to web application development, allowing developers to focus on building the app’s functionality without having to deal with the low-level details. In our chess app, we use Django to handle various aspects of the backend, including routing, handling HTTP requests, and managing data models.
To create a new Django project and app:

```bash
django-admin startproject chess_game
cd chess_game
django-admin startapp game
```

For more in-depth details on how Django works, you can visit the official Django documentation: https://www.djangoproject.com/start/

####  2.2. Breakdown of the Django structure
After create the Django project and app, the directory structure for your new Django project will look like this out-of-the-box:
```markdown
chess_game/
├── chess_game/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── game/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
├── manage.py
```
##### chess_game/ (Outer directory):

  * This is the root directory of your project.

##### chess_game/ (Inner directory):

  * This directory contains the actual Django project. It’s where all your core project files and settings are located.
  * ```__init__.py```: This file marks the directory as a Python package.
  * ```asgi.py```: ASGI configuration for asynchronous support (used for deploying with ASGI servers).
  * ```settings.py```: This is where you configure your project's settings, such as database settings, installed apps, middleware, and more.
  * ```urls.py```: This file handles the routing for your project, linking URLs to views.
  * ```wsgi.py```: WSGI configuration for deploying the application with a WSGI server.
  * ```manage.py```: This is a command-line utility that helps with various administrative tasks such as running the server, applying database migrations, and creating apps.

##### game/ (App Directory)
* ```models.py```: Where you will define your database models (e.g., ChessGame).
* ```views.py```: Where you will define the logic for handling HTTP requests and responses.
* ```urls.py```: Where you will define URLs that map to specific views for your app.
* ```admin.py```: To register models with the Django admin interface.
* ```apps.py```: Contains the configuration for your app.

This is the basic structure that Django sets up when you create a new project. As you add apps, models, views, and other files, this structure will grow and become more organized.

#### 2.3. Set Up MongoDB Database in Django

Ensure you have MongoDB installed and running on your machine, see more details: https://www.mongodb.com/docs/manual/installation/.

For example, to install/start MongoDB on macOS:

(Reference: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
```bash
brew update
brew upgrade
brew tap mongodb/brew
brew install mongodb-community@8.0
brew services start mongodb/brew/mongodb-community
brew services list
mongod --version # once installed, show the mongoDB version
```

If you prefer a simpler setup, there’s another option to use MongoDB Atlas, a cloud-based MongoDB service, which provides a fully managed database solution that eliminates the need to set up and maintain a local MongoDB instance. This can be an easier option for those new to MongoDB or looking for a hassle-free setup. For more details: https://www.mongodb.com/docs/atlas/getting-started/

In ```chess_game/settings.py```, add the following changes:

```python
INSTALLED_APPS = [
    ...,
    'corsheaders',
    'rest_framework',
    'game',
    'channels',
]

ASGI_APPLICATION = 'chess_game.asgi.application'

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

# MongoDB connection settings (will be handled in Django-provided ```views.py``` with PyMongo)
DATABASES = {}
# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017'
DB_NAME = 'chess_db'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # Make sure this includes the base static directory
]
```

#### 2.3. Create ASGI Configuration:

In the project’s root directory, create a file named ```asgi.py```.
Now in Pycharm (recommended IDE for Python development, or you can choose another depending on your preferences), we can begin to configure Django channels:

```python
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
```

#### 2.4. Create Consumer for WebSocket Communication:

WebSockets are a technology that enables full-duplex communication (bidirectional data transfer) over a single, long-lived connection between a client (such as a browser) and a server. Unlike traditional HTTP connections, where the client has to repeatedly request data from the server (using polling or AJAX), WebSockets allow both the server and client to send and receive data in real-time, without needing to repeatedly open new connections.

This technology is essential for building interactive web applications, especially ones that require real-time updates, such as online games (like chess), chats, or live data feeds.

In ```chess/consumers.py```, create a consumer to handle WebSocket connections. The consumer will manage sending and receiving game moves. The consumer will be responsible for both receiving messages (such as game moves) and sending messages (such as updates to the game state or move notifications). A key part of the consumer is handling messages sent by the client. When a player makes a move, the message will be sent through the WebSocket connection to the server.

```python
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
```



### 3. Design Models for Chess Game

In the Django-provided ```game/models.py```, we will define a model to store the state of the chess game. In Django, a model is a Python class that defines the structure of your application's data. It acts as the bridge between your application and the database, specifying how data is stored, retrieved, and manipulated. A model represents a single table in the database, and each attribute of the model corresponds to a column in that table. This will include the position of each piece and the current turn.

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

In Django-provided ```game/views.py```:

```python
from django.shortcuts import render

def chess_game(request):
    return render(request, 'chess_game/index.html')

```


### 4. Define URLs for the views:

In the Django-provided ```game/urls.py```, add the following to map the views to URLs:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chess_game, name='chess_game'),
]
```
Also, add ```game.urls``` to the main ```chess_game/urls.py```:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chess_game/', include('chess_game.urls')),  # Include chess_game URLs
]
```

#### 5.2. Templates for the Board

Create a template file via ```game/templates/index.html``` to render the chess game template, where you will embed the Javascript game board. Run the following command from the root directory of your project.

```bash
mkdir -p game/templates
```


Add the following HTML to ```game/templates/index.html```:

```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess Game</title>
    <style>
        /* Simple styles for the page and chessboard container */
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #board1 {
            width: 400px;
            height: 400px;
        }
    </style>
</head>
<body>
    <h1>Chess Game</h1>

    <!-- Chessboard container where the board will be rendered -->
    <div id="board1"></div>

    <!-- Load Chessboard.js from CDN -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/kevinludwig/pgn-parser/dist/pgn-parser.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js"></script> -->
   <script src="{% static 'js/chessboard-1.0.0.min.js' %}"></script>
<script src="https://cdn.jsdelivr.net/gh/jbkunst/chessboardjs-themes/chessboardjs-themes.js"></script>
<div id="board1" style="width: 180px"></div>


    <script>
        // Ensure that the Chessboard.js script is fully loaded before initialization
        window.onload = function() {
            // Check if Chessboard is available
            if (typeof Chessboard !== 'undefined') {
                var board = Chessboard('board1', {
                    draggable: true,    // Allow pieces to be dragged
                    dropOffBoard: 'trash',  // Drop pieces off the board
                    sparePieces: true    // Allow pieces to be dragged outside the board
                });

                // Start the game by setting up the pieces on the board
                board.start();
            } else {
                console.error("Chessboard.js failed to load.");
            }
        };
    </script>
</body>
</html>
```

Add the following minified JS to ```chess_game/static/js/chessboard-1.0.0.min.js```. This JavaScript file contains logic for rendering the chessboard on the webpage, handling moves, and interacting with the server in real time (e.g., via WebSockets).

```javascript
!function(){"use strict";var z=window.jQuery,F="abcdefgh".split(""),r=20,A="…",W="1.8.3",e="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",G=pe(e),n=200,t=200,o=60,a=30,i=100,H={};function V(e,r,n){function t(){o=0,a&&(a=!1,s())}var o=0,a=!1,i=[],s=function(){o=window.setTimeout(t,r),e.apply(n,i)};return function(e){i=arguments,o?a=!0:s()}}function Z(){return"xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx".replace(/x/g,function(e){return(16*Math.random()|0).toString(16)})}function _(e){return JSON.parse(JSON.stringify(e))}function s(e){var r=e.split(".");return{major:parseInt(r[0],10),minor:parseInt(r[1],10),patch:parseInt(r[2],10)}}function ee(e,r){for(var n in r)if(r.hasOwnProperty(n))for(var t="{"+n+"}",o=r[n];-1!==e.indexOf(t);)e=e.replace(t,o);return e}function re(e){return"string"==typeof e}function ne(e){return"function"==typeof e}function p(e){return"number"==typeof e&&isFinite(e)&&Math.floor(e)===e}function c(e){return"fast"===e||"slow"===e||!!p(e)&&0<=e}function te(e){if(!re(e))return!1;var r=e.split("-");return 2===r.length&&(oe(r[0])&&oe(r[1]))}function oe(e){return re(e)&&-1!==e.search(/^[a-h][1-8]$/)}function u(e){return re(e)&&-1!==e.search(/^[bw][KQRNBP]$/)}function ae(e){if(!re(e))return!1;var r=(e=function(e){return e.replace(/8/g,"11111111").replace(/7/g,"1111111").replace(/6/g,"111111").replace(/5/g,"11111").replace(/4/g,"1111").replace(/3/g,"111").replace(/2/g,"11")}(e=e.replace(/ .+$/,""))).split("/");if(8!==r.length)return!1;for(var n=0;n<8;n++)if(8!==r[n].length||-1!==r[n].search(/[^kqrnbpKQRNBP1]/))return!1;return!0}function ie(e){if(!z.isPlainObject(e))return!1;for(var r in e)if(e.hasOwnProperty(r)&&(!oe(r)||!u(e[r])))return!1;return!0}function se(){return typeof window.$&&z.fn&&z.fn.jquery&&function(e,r){e=s(e),r=s(r);var n=1e5*e.major*1e5+1e5*e.minor+e.patch;return 1e5*r.major*1e5+1e5*r.minor+r.patch<=n}(z.fn.jquery,W)}function pe(e){if(!ae(e))return!1;for(var r,n=(e=e.replace(/ .+$/,"")).split("/"),t={},o=8,a=0;a<8;a++){for(var i=n[a].split(""),s=0,p=0;p<i.length;p++){if(-1!==i[p].search(/[1-8]/))s+=parseInt(i[p],10);else t[F[s]+o]=(r=i[p]).toLowerCase()===r?"b"+r.toUpperCase():"w"+r.toUpperCase(),s+=1}o-=1}return t}function ce(e){if(!ie(e))return!1;for(var r,n,t="",o=8,a=0;a<8;a++){for(var i=0;i<8;i++){var s=F[i]+o;e.hasOwnProperty(s)?t+=(r=e[s],n=void 0,"w"===(n=r.split(""))[0]?n[1].toUpperCase():n[1].toLowerCase()):t+="1"}7!==a&&(t+="/"),o-=1}return t=function(e){return e.replace(/11111111/g,"8").replace(/1111111/g,"7").replace(/111111/g,"6").replace(/11111/g,"5").replace(/1111/g,"4").replace(/111/g,"3").replace(/11/g,"2")}(t)}function ue(e,r,n){for(var t=function(e){for(var r=[],n=0;n<8;n++)for(var t=0;t<8;t++){var o=F[n]+(t+1);e!==o&&r.push({square:o,distance:(a=e,i=o,void 0,void 0,void 0,void 0,void 0,void 0,void 0,void 0,s=a.split(""),p=F.indexOf(s[0])+1,c=parseInt(s[1],10),u=i.split(""),f=F.indexOf(u[0])+1,d=parseInt(u[1],10),h=Math.abs(p-f),l=Math.abs(c-d),l<=h?h:l)})}var a,i,s,p,c,u,f,d,h,l;r.sort(function(e,r){return e.distance-r.distance});var v=[];for(n=0;n<r.length;n++)v.push(r[n].square);return v}(n),o=0;o<t.length;o++){var a=t[o];if(e.hasOwnProperty(a)&&e[a]===r)return a}return!1}function fe(e){return"black"!==e.orientation&&(e.orientation="white"),!1!==e.showNotation&&(e.showNotation=!0),!0!==e.draggable&&(e.draggable=!1),"trash"!==e.dropOffBoard&&(e.dropOffBoard="snapback"),!0!==e.sparePieces&&(e.sparePieces=!1),e.sparePieces&&(e.draggable=!0),e.hasOwnProperty("pieceTheme")&&(re(e.pieceTheme)||ne(e.pieceTheme))||(e.pieceTheme="https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png"),c(e.appearSpeed)||(e.appearSpeed=n),c(e.moveSpeed)||(e.moveSpeed=t),c(e.snapbackSpeed)||(e.snapbackSpeed=o),c(e.snapSpeed)||(e.snapSpeed=a),c(e.trashSpeed)||(e.trashSpeed=i),function(e){return p(e)&&1<=e}(e.dragThrottleRate)||(e.dragThrottleRate=r),e}H.alpha="alpha-d2270",H.black="black-3c85d",H.board="board-b72b1",H.chessboard="chessboard-63f37",H.clearfix="clearfix-7da63",H.highlight1="highlight1-32417",H.highlight2="highlight2-9c5d2",H.notation="notation-322f9",H.numeric="numeric-fc462",H.piece="piece-417db",H.row="row-5277c",H.sparePieces="spare-pieces-7492f",H.sparePiecesBottom="spare-pieces-bottom-ae20f",H.sparePiecesTop="spare-pieces-top-4028b",H.square="square-55d63",H.white="white-1e1d7",window.Chessboard=function(e,f){if(!function(){if(se())return!0;var e="Chessboard Error 1005: Unable to find a valid version of jQuery. Please include jQuery "+W+" or higher on the page\n\nExiting"+A;return window.alert(e),!1}())return null;var n=function(e){if(""===e){var r="Chessboard Error 1001: The first argument to Chessboard() cannot be an empty string.\n\nExiting"+A;return window.alert(r),!1}re(e)&&"#"!==e.charAt(0)&&(e="#"+e);var n=z(e);if(1===n.length)return n;var t="Chessboard Error 1003: The first argument to Chessboard() must be the ID of a DOM node, an ID query selector, or a single DOM node.\n\nExiting"+A;return window.alert(t),!1}(e);if(!n)return null;f=fe(f=function(e){return"start"===e?e={position:_(G)}:ae(e)?e={position:pe(e)}:ie(e)&&(e={position:_(e)}),z.isPlainObject(e)||(e={}),e}(f));var r=null,a=null,t=null,o=null,i={},s=2,p="white",c={},u=null,d=null,h=null,l=!1,v={},g={},w={},b=16;function m(e,r,n){if(!0===f.hasOwnProperty("showErrors")&&!1!==f.showErrors){var t="Chessboard Error "+e+": "+r;return"console"===f.showErrors&&"object"==typeof console&&"function"==typeof console.log?(console.log(t),void(2<=arguments.length&&console.log(n))):"alert"===f.showErrors?(n&&(t+="\n\n"+JSON.stringify(n)),void window.alert(t)):void(ne(f.showErrors)&&f.showErrors(e,r,n))}}function P(e){return ne(f.pieceTheme)?f.pieceTheme(e):re(f.pieceTheme)?ee(f.pieceTheme,{piece:e}):(m(8272,"Unable to build image source for config.pieceTheme."),"")}function y(e,r,n){var t='<img src="'+P(e)+'" ';return re(n)&&""!==n&&(t+='id="'+n+'" '),t+='alt="" class="{piece}" data-piece="'+e+'" style="width:'+b+"px;height:"+b+"px;",r&&(t+="display:none;"),ee(t+='" />',H)}function x(e){var r=["wK","wQ","wR","wB","wN","wP"];"black"===e&&(r=["bK","bQ","bR","bB","bN","bP"]);for(var n="",t=0;t<r.length;t++)n+=y(r[t],!1,v[r[t]]);return n}function O(e,r,n,t){var o=z("#"+g[e]),a=o.offset(),i=z("#"+g[r]),s=i.offset(),p=Z();z("body").append(y(n,!0,p));var c=z("#"+p);c.css({display:"",position:"absolute",top:a.top,left:a.left}),o.find("."+H.piece).remove();var u={duration:f.moveSpeed,complete:function(){i.append(y(n)),c.remove(),ne(t)&&t()}};c.animate(s,u)}function S(e,r,n){var t=z("#"+v[e]).offset(),o=z("#"+g[r]),a=o.offset(),i=Z();z("body").append(y(e,!0,i));var s=z("#"+i);s.css({display:"",position:"absolute",left:t.left,top:t.top});var p={duration:f.moveSpeed,complete:function(){o.find("."+H.piece).remove(),o.append(y(e)),s.remove(),ne(n)&&n()}};s.animate(a,p)}function T(){for(var e in r.find("."+H.piece).remove(),c)c.hasOwnProperty(e)&&z("#"+g[e]).append(y(c[e]))}function q(){r.html(function(e){"black"!==e&&(e="white");var r="",n=_(F),t=8;"black"===e&&(n.reverse(),t=1);for(var o="white",a=0;a<8;a++){r+='<div class="{row}">';for(var i=0;i<8;i++){var s=n[i]+t;r+='<div class="{square} '+H[o]+" square-"+s+'" style="width:'+b+"px;height:"+b+'px;" id="'+g[s]+'" data-square="'+s+'">',f.showNotation&&(("white"===e&&1===t||"black"===e&&8===t)&&(r+='<div class="{notation} {alpha}">'+n[i]+"</div>"),0===i&&(r+='<div class="{notation} {numeric}">'+t+"</div>")),r+="</div>",o="white"===o?"black":"white"}r+='<div class="{clearfix}"></div></div>',o="white"===o?"black":"white","white"===e?t-=1:t+=1}return ee(r,H)}(p,f.showNotation)),T(),f.sparePieces&&("white"===p?(t.html(x("black")),o.html(x("white"))):(t.html(x("white")),o.html(x("black"))))}function k(e){var r=_(c),n=_(e);ce(r)!==ce(n)&&(ne(f.onChange)&&f.onChange(r,n),c=e)}function E(e,r){for(var n in w)if(w.hasOwnProperty(n)){var t=w[n];if(e>=t.left&&e<t.left+b&&r>=t.top&&r<t.top+b)return n}return"offboard"}function C(){r.find("."+H.square).removeClass(H.highlight1+" "+H.highlight2)}function B(){C();var e=_(c);delete e[h],k(e),T(),a.fadeOut(f.trashSpeed),l=!1}function I(e,r,n,t){ne(f.onDragStart)&&!1===f.onDragStart(e,r,_(c),p)||(l=!0,u=r,d="spare"===(h=e)?"offboard":e,function(){for(var e in w={},g)g.hasOwnProperty(e)&&(w[e]=z("#"+g[e]).offset())}(),a.attr("src",P(r)).css({display:"",position:"absolute",left:n-b/2,top:t-b/2}),"spare"!==e&&z("#"+g[e]).addClass(H.highlight1).find("."+H.piece).css("display","none"))}function M(e,r){a.css({left:e-b/2,top:r-b/2});var n=E(e,r);n!==d&&(oe(d)&&z("#"+g[d]).removeClass(H.highlight2),oe(n)&&z("#"+g[n]).addClass(H.highlight2),ne(f.onDragMove)&&f.onDragMove(n,d,h,u,_(c),p),d=n)}function N(e){var r="drop";if("offboard"===e&&"snapback"===f.dropOffBoard&&(r="snapback"),"offboard"===e&&"trash"===f.dropOffBoard&&(r="trash"),ne(f.onDrop)){var n=_(c);"spare"===h&&oe(e)&&(n[e]=u),oe(h)&&"offboard"===e&&delete n[h],oe(h)&&oe(e)&&(delete n[h],n[e]=u);var t=_(c),o=f.onDrop(h,e,u,n,t,p);"snapback"!==o&&"trash"!==o||(r=o)}"snapback"===r?function(){if("spare"!==h){C();var e=z("#"+g[h]).offset(),r={duration:f.snapbackSpeed,complete:function(){T(),a.css("display","none"),ne(f.onSnapbackEnd)&&f.onSnapbackEnd(u,h,_(c),p)}};a.animate(e,r),l=!1}else B()}():"trash"===r?B():"drop"===r&&function(e){C();var r=_(c);delete r[h],r[e]=u,k(r);var n=z("#"+g[e]).offset(),t={duration:f.snapSpeed,complete:function(){T(),a.css("display","none"),ne(f.onSnapEnd)&&f.onSnapEnd(h,e,u)}};a.animate(n,t),l=!1}(e)}function j(e){e.preventDefault()}function D(e){if(f.draggable){var r=z(this).attr("data-square");oe(r)&&c.hasOwnProperty(r)&&I(r,c[r],e.pageX,e.pageY)}}function R(e){if(f.draggable){var r=z(this).attr("data-square");oe(r)&&c.hasOwnProperty(r)&&(e=e.originalEvent,I(r,c[r],e.changedTouches[0].pageX,e.changedTouches[0].pageY))}}function Q(e){f.sparePieces&&I("spare",z(this).attr("data-piece"),e.pageX,e.pageY)}function X(e){f.sparePieces&&I("spare",z(this).attr("data-piece"),(e=e.originalEvent).changedTouches[0].pageX,e.changedTouches[0].pageY)}i.clear=function(e){i.position({},e)},i.destroy=function(){n.html(""),a.remove(),n.unbind()},i.fen=function(){return i.position("fen")},i.flip=function(){return i.orientation("flip")},i.move=function(){if(0!==arguments.length){for(var e=!0,r={},n=0;n<arguments.length;n++)if(!1!==arguments[n])if(te(arguments[n])){var t=arguments[n].split("-");r[t[0]]=t[1]}else m(2826,"Invalid move passed to the move method.",arguments[n]);else e=!1;var o=function(e,r){var n=_(e);for(var t in r)if(r.hasOwnProperty(t)&&n.hasOwnProperty(t)){var o=n[t];delete n[t],n[r[t]]=o}return n}(c,r);return i.position(o,e),o}},i.orientation=function(e){return 0===arguments.length?p:"white"===e||"black"===e?(p=e,q(),p):"flip"===e?(p="white"===p?"black":"white",q(),p):void m(5482,"Invalid value passed to the orientation method.",e)},i.position=function(e,r){if(0===arguments.length)return _(c);if(re(e)&&"fen"===e.toLowerCase())return ce(c);(re(e)&&"start"===e.toLowerCase()&&(e=_(G)),ae(e)&&(e=pe(e)),ie(e))?(!1!==r&&(r=!0),r?(function(e,r,n){if(0!==e.length)for(var t=0,o=0;o<e.length;o++){var a=e[o];"clear"===a.type?z("#"+g[a.square]+" ."+H.piece).fadeOut(f.trashSpeed,i):"add"!==a.type||f.sparePieces?"add"===a.type&&f.sparePieces?S(a.piece,a.square,i):"move"===a.type&&O(a.source,a.destination,a.piece,i):z("#"+g[a.square]).append(y(a.piece,!0)).find("."+H.piece).fadeIn(f.appearSpeed,i)}function i(){(t+=1)===e.length&&(T(),ne(f.onMoveEnd)&&f.onMoveEnd(_(r),_(n)))}}(function(e,r){e=_(e),r=_(r);var n=[],t={};for(var o in r)r.hasOwnProperty(o)&&e.hasOwnProperty(o)&&e[o]===r[o]&&(delete e[o],delete r[o]);for(o in r)if(r.hasOwnProperty(o)){var a=ue(e,r[o],o);a&&(n.push({type:"move",source:a,destination:o,piece:r[o]}),delete e[a],delete r[o],t[o]=!0)}for(o in r)r.hasOwnProperty(o)&&(n.push({type:"add",square:o,piece:r[o]}),delete r[o]);for(o in e)e.hasOwnProperty(o)&&(t.hasOwnProperty(o)||(n.push({type:"clear",square:o,piece:e[o]}),delete e[o]));return n}(c,e),c,e),k(e)):(k(e),T())):m(6482,"Invalid value passed to the position method.",e)},i.resize=function(){b=function(){var e=parseInt(n.width(),10);if(!e||e<=0)return 0;for(var r=e-1;r%8!=0&&0<r;)r-=1;return r/8}(),r.css("width",8*b+"px"),a.css({height:b,width:b}),f.sparePieces&&n.find("."+H.sparePieces).css("paddingLeft",b+s+"px"),q()},i.start=function(e){i.position("start",e)};var Y=V(function(e){l&&M(e.pageX,e.pageY)},f.dragThrottleRate),K=V(function(e){l&&(e.preventDefault(),M(e.originalEvent.changedTouches[0].pageX,e.originalEvent.changedTouches[0].pageY))},f.dragThrottleRate);function L(e){l&&N(E(e.pageX,e.pageY))}function U(e){l&&N(E(e.originalEvent.changedTouches[0].pageX,e.originalEvent.changedTouches[0].pageY))}function $(e){if(!l&&ne(f.onMouseoverSquare)){var r=z(e.currentTarget).attr("data-square");if(oe(r)){var n=!1;c.hasOwnProperty(r)&&(n=c[r]),f.onMouseoverSquare(r,n,_(c),p)}}}function J(e){if(!l&&ne(f.onMouseoutSquare)){var r=z(e.currentTarget).attr("data-square");if(oe(r)){var n=!1;c.hasOwnProperty(r)&&(n=c[r]),f.onMouseoutSquare(r,n,_(c),p)}}}return p=f.orientation,f.hasOwnProperty("position")&&("start"===f.position?c=_(G):ae(f.position)?c=pe(f.position):ie(f.position)?c=_(f.position):m(7263,"Invalid value passed to config.position.",f.position)),function(){!function(){for(var e=0;e<F.length;e++)for(var r=1;r<=8;r++){var n=F[e]+r;g[n]=n+"-"+Z()}var t="KQRNBP".split("");for(e=0;e<t.length;e++){var o="w"+t[e],a="b"+t[e];v[o]=o+"-"+Z(),v[a]=a+"-"+Z()}}(),n.html(function(e){var r='<div class="{chessboard}">';return e&&(r+='<div class="{sparePieces} {sparePiecesTop}"></div>'),r+='<div class="{board}"></div>',e&&(r+='<div class="{sparePieces} {sparePiecesBottom}"></div>'),ee(r+="</div>",H)}(f.sparePieces)),r=n.find("."+H.board),f.sparePieces&&(t=n.find("."+H.sparePiecesTop),o=n.find("."+H.sparePiecesBottom));var e=Z();z("body").append(y("wP",!0,e)),a=z("#"+e),s=parseInt(r.css("borderLeftWidth"),10),i.resize()}(),function(){z("body").on("mousedown mousemove","."+H.piece,j),r.on("mousedown","."+H.square,D),n.on("mousedown","."+H.sparePieces+" ."+H.piece,Q),r.on("mouseenter","."+H.square,$).on("mouseleave","."+H.square,J);var e=z(window);e.on("mousemove",Y).on("mouseup",L),"ontouchstart"in document.documentElement&&(r.on("touchstart","."+H.square,R),n.on("touchstart","."+H.sparePieces+" ."+H.piece,X),e.on("touchmove",K).on("touchend",U))}(),i},window.ChessBoard=window.Chessboard,window.Chessboard.fenToObj=pe,window.Chessboard.objToFen=ce}();
```

### 6. Run the Development Server
Since we're using MongoDB directly with ```PyMongo```, no migrations are needed. You can now run the Django server:

```bash
python manage.py runserver
```

### 7. View chess game
Open in your browser: http://localhost:8000/



### 8. Conclusion
Congratulations! You’ve just built a simple yet powerful chess app using Django and MongoDB. You now have a functioning backend that tracks game data and a basic frontend to visualize the chessboard. This project gave you experience in connecting Django with MongoDB, designing a chess game model, and creating API endpoints for game actions. Of course, this is just the beginning—you can enhance this app by adding features like player authentication, real-time gameplay (with WebSockets), and advanced chess logic. By following this tutorial, you’ve built the foundation for a dynamic, scalable chess application that could grow into a fully-fledged game platform. Happy coding, and may your next move be your best!
, you've created a functional chess game with a player vs. AI bot interaction, backed by Django, Django Channels, MongoDB, and an AI bot using Stockfish