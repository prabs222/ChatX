from django.urls import path
from .views import *

urlpatterns = [
    path('', getRoutes ),
    path('home/', home),
    
    # Admin Urls
    path('admins/topics/', TopicAPIView.as_view(), name='topic_list'),
    path('admins/topics/<int:pk>/', TopicDetailAPIView.as_view(), name='topic_detail'),
    path('admins/rooms/', AdminRoomAPIView.as_view(), name='room_list'),
    path('admins/rooms/<int:pk>/', AdminRoomDetailAPIView.as_view(), name='room_detail'),

    # Rooms
    path('rooms/', RoomAPIView.as_view(), name='get_rooms'),
    path('rooms/<str:pk>/', RoomAPIView.as_view(), name='get_room'),
    path('join-room/<str:pk>/', RoomAPIView.as_view(), name='join_room'),
    path('topic-rooms/', topicWiseRooms ),
    path('my-rooms/', getMyRooms),
    path('other-rooms/', getOtherRooms),
    
    # Messages
    path('get-messages/<str:room_id>/', get_messages, name='get_messages')
]
