from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import TopicSerializer, UserGetSerializer, ChatSerializer, RoomSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room, Message, Topic

User = get_user_model()


@api_view(["GET"])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def home(request):
    rooms = Room.objects.exclude(participants=request.user)
    roomSerializer = RoomSerializer(rooms, many=True)
    topics = Topic.objects.all()
    topicsSerializer = TopicSerializer(topics, many=True)

    return Response({'rooms': roomSerializer.data, 'topics': topicsSerializer.data})


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def topicWiseRooms(request):
    topic_id = request.query_params.get('topic_id', None)
    if topic_id:
        topic = Topic.objects.get(id=topic_id)
        rooms = Room.objects.filter(topic=topic)
        roomSerializer = RoomSerializer(rooms, many=True)
        return Response(roomSerializer.data)
    else:
        return Response({"detail": "topic not present"}, status=status.HTTP_400_BAD_REQUEST)


class RoomAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            return self.get_room(request, pk)
        else:
            return self.get_rooms(request)

    def get_rooms(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def get_room(self, request, pk):
        try:
            room = Room.objects.get(id=pk)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            room = Room.objects.get(id=pk)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        room.participants.add(request.user)
        serializer = RoomSerializer(room)
        return Response(serializer.data)



@api_view(('GET',))
@permission_classes([IsAuthenticated])
def getMyRooms(request):
    rooms = Room.objects.filter(participants=request.user)
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def getOtherRooms(request):
    rooms = Room.objects.exclude(participants=request.user)
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 30

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    if request.method == 'GET':
        try:
            user_obj = User.objects.exclude(id=request.user.id)
            seralizer = UserGetSerializer(user_obj, many=True)
            return Response(seralizer.data)
        except Exception as e:
            print(e)
            return Response(seralizer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, room_id):
    if request.method == 'GET':
        try:
            room = Room.objects.get(id=room_id)
            chats = Message.objects.filter(room=room)
            paginator = CustomPagination()
            results = paginator.paginate_queryset(chats, request)
            serializer = ChatSerializer(results, many=True)
            
            room_name = room.name

            response_data = {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "room_name": room_name, 
                "results": serializer.data
            }

            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TopicAPIView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]
    

class TopicDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]



class AdminRoomAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser]


class AdminRoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser]
