from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from django.db import models
from chat.ModelsAi import ModelAI
from chat.Conversation import Conversation
from chat.models import Language

class TextTranMessage(models.Model):
    code = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.TextField()
    provider = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class MessageAI(models.Model):
    text = models.TextField()
    text_tran = models.ManyToManyField(TextTranMessage, blank=True)
    model = models.ForeignKey(ModelAI, on_delete=models.CASCADE)
    is_like = models.BooleanField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MessageUser(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    text_tran = models.ManyToManyField(TextTranMessage, blank=True)
    image_path =  models.CharField(max_length=255 , blank=True)
    message_ai = models.ManyToManyField(MessageAI)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class TextTranMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTranMessage
        fields = '__all__'
        
class MessageUserSerializer(serializers.ModelSerializer):
    text_tran_info = TextTranMessageSerializer(source='text_tran', read_only=True, many=True)
    class Meta:
        model = MessageUser
        fields = '__all__'

class MessageAISerializer(serializers.ModelSerializer):
    text_tran_info = TextTranMessageSerializer(source='text_tran', read_only=True, many=True)
    class Meta:
        model = MessageAI
        fields = '__all__'
class ListMessagesSerializer(serializers.ModelSerializer):
    message_ai_info = MessageAISerializer(source='message_ai', read_only=True, many=True)
    text_tran_info = TextTranMessageSerializer(source='text_tran', read_only=True, many=True)
    
    current_index = serializers.SerializerMethodField()

    class Meta:
        model = MessageUser
        fields = '__all__'

    def get_current_index(self, obj):
        return 0

    def to_representation(self, instance):
        representation = super(ListMessagesSerializer, self).to_representation(instance)
        message_ai_info = representation.pop('message_ai_info', [])
        current_index = representation.pop('current_index', None)
        text_tran_info = representation.pop('text_tran_info', [])  # Include text_tran_info

        message_user_info = {
            'message_user': {
                **representation,
                'text_tran_info': text_tran_info,  # Include text_tran_info under message_user
            },
            'message_ai': message_ai_info,
            'current_index': current_index,
        }

        return message_user_info


class ListMessagesAPIViewSet(viewsets.ModelViewSet):
    queryset = MessageUser.objects.all()
    serializer_class = ListMessagesSerializer
    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = MessageUser.objects.filter(conversation__id=conversation_id)
        else:
            queryset = MessageUser.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            return Response(data, status=200)
        except Exception as e:
            return Response(str(e), status=500)
