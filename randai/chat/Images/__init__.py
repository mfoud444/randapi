from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from django.db import models
from chat.ModelsAi import ModelAI
from chat.Messages import TextTranMessage , TextTranMessageSerializer
from chat.Conversation import Conversation

class ImageAI(models.Model):
    image_path = models.CharField(max_length=255)
    model = models.ForeignKey(ModelAI, on_delete=models.CASCADE)
    is_like = models.BooleanField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class MessageUserImage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text_tran = models.ManyToManyField(TextTranMessage, blank=True)
    text = models.CharField(max_length=255)
    image_ai = models.ManyToManyField(ImageAI)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ImageAISerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAI
        fields = '__all__'

class MessageUserImageSerializer(serializers.ModelSerializer):
    text_tran_info = TextTranMessageSerializer(source='text_tran', read_only=True, many=True)
    class Meta:
        model = MessageUserImage
        fields = '__all__'


class ListImageAISerializer(serializers.ModelSerializer):
    message_ai_info = ImageAISerializer(source='image_ai', read_only=True, many=True)
    current_index = serializers.SerializerMethodField()

    class Meta:
        model = MessageUserImage
        fields = '__all__'

    def get_current_index(self, obj):
        return 0

    def to_representation(self, instance):
        representation = super(ListImageAISerializer, self).to_representation(instance)
        message_ai_info = representation.pop('message_ai_info', [])
        current_index = representation.pop('current_index', None)

        message_user_info = {
            'message_user': representation,
            'message_ai': message_ai_info,
            'current_index': current_index,
        }

        return message_user_info



class ListImageAIAPIViewSet(viewsets.ModelViewSet):
    queryset = MessageUserImage.objects.all()
    serializer_class = ListImageAISerializer
    def get_queryset(self):

        conversation_id = self.request.query_params.get('conversation_id')

        if conversation_id:
            queryset = MessageUserImage.objects.filter(conversation__id=conversation_id)
        else:
            queryset = MessageUserImage.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            return Response(data, status=200)
        except Exception as e:
            return Response(str(e), status=500)
