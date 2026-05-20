from django.urls import path
from .views import book_room

urlpatterns = [
    path('<int:room_id>/', book_room, name='book_room'),
]