from rest_framework import serializers
from .models import Room, Message, Topic
from django.contrib.auth import get_user_model


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
     
     
class UserGetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'id', 'name']
        extra_kwargs = {'id': {'read_only': True}}


class ChatSerializer(serializers.ModelSerializer):
    user = UserGetSerializer()
    room = RoomSerializer()
    
    class Meta:
        model = Message()
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True}}
        