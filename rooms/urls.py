from django.urls import path

from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('manage/', views.manage_rooms, name='manage_rooms'),
    path('manage/new/', views.edit_room, name='room_create'),
    path('manage/<int:room_id>/edit/', views.edit_room, name='room_edit'),
]
