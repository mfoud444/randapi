from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers

class Notification(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField() 
    type = models.CharField(max_length=255)  
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'