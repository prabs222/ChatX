from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name
    
class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self) -> str:
        return self.name
        
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self) -> str:
        return self.message[0:50]