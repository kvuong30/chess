from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chess_game/', include('chess_game.urls')),  # Include chess_game URLs
]
