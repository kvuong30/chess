## Chess App with Django + MongoDB

### 1. Setting Up the Project Environment
#### 1.1 Prerequisites:
* **Python 3.7+**
* **Django**: Open-source web framework
* **MongoDB**: NoSQL database to store game data (using ```pymongo``` to integrate MongoDB with Django)
* **Python packages**:
  * django
  * djangorestframework
  * pymongo
  * django-cors-headers (for handling Cross-Origin Resource Sharing, or CORS)
  * chess (Python chess library)
  * channels_redis

#### 1.2 Create virtual environment

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

#### 2. Set Up MongoDB Database in Django

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


### 3. Run the Development Server
Since we're using MongoDB directly with ```PyMongo```, no migrations are needed. We can now run the Django server:

```bash
python manage.py runserver
```

### 4. View chess game
Open in your browser: http://localhost:8000/chess_game
