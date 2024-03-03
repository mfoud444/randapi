from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.db import models
import uuid
from chat.models import Language , Prompt
from chat.ModelsAi import ModelAI , ModelAISerializer
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from util import  Settings


settings = Settings()
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(blank=True, null=True)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=10, choices=settings.TYPE_CHOICES, default='text')
    model = models.ForeignKey(ModelAI, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    is_pin = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    is_like = models.BooleanField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



class ConversationSerializer(serializers.ModelSerializer):
    model_info = ModelAISerializer(source='model', read_only=True)
    chat = serializers.SerializerMethodField()
    # type = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_chat(self, obj):
        chat = []
        return chat

class ConversationAPIViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        try:
           
            user_id = request.query_params.get('user_id')
            types = request.query_params.getlist('type')
            print("user_id", user_id)
            print("types:", types)

            # Filtering the queryset based on userId
            queryset = self.get_queryset().filter(user_id=user_id,type=types[0]).order_by('-updated_at')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            return Response(data, status=200)
        except Exception as e:
            return Response(str(e), status=500)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            title = request.data.get('title', None)
            is_like = request.data.get('is_like', None)
            is_pin = request.data.get('is_pin', None)
            print("title", title)
            if title is not None:
                print("title222", title)
                instance.title = title
                instance.save()
                return Response(status=200)
            elif is_like is not None:
                instance.is_like = is_like
                instance.save()
                return Response(status=200)
            elif is_pin is not None:
                instance.is_pin = is_pin
                instance.save()
                
                # serializer = self.get_serializer(instance)
                return Response(status=200)
            else:
                return Response("Title is required for update", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view
@api_view(['DELETE'])
def delete_conversation(request, user_id, type):
    try:
        conversation = Conversation.objects.filter(user_id=user_id, type=type)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
    conversation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
