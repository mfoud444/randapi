# myapp/serializers.py
from rest_framework import serializers
from .models import *


class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = '__all__'

class ApiOptionSerializer(serializers.ModelSerializer):
    keys = ApiKeySerializer(source='api_key', many=True,  default=None)
    class Meta:
        model = ApiOption
        fields = '__all__'




class ApiOwnerSerializer(serializers.ModelSerializer):
    api_options = ApiOptionSerializer(source='api_options_id',read_only=True,  many=True, required=False)
    class Meta:
        model = ApiOwner
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CompanyAISerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAI
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'



class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = '__all__'










class ChatTextSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField(allow_null=True, required=False, default=None)
    user_id = serializers.CharField(required=True)
    parent_message_id = serializers.IntegerField(required=False)
    model = serializers.CharField(required=False)
    prompt = serializers.CharField(required=True)
    is_stream = serializers.BooleanField(required=False)
    provider_id = serializers.IntegerField(required=False)
    system_message = serializers.CharField(required=False, allow_blank=True)
    temperature = serializers.FloatField(required=False)
    top_p = serializers.FloatField(required=False)
    api_owner = serializers.CharField(required=False)
    lang = serializers.CharField(required=False, allow_null=True)
    is_web_search  = serializers.BooleanField(required=False)
    image = serializers.CharField(required=False, allow_null=True,  allow_blank=True)
    is_emojis = serializers.BooleanField(required=False)
    is_group_telegram = serializers.BooleanField(required=False)

class DocumentclassSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    conversation_id = serializers.UUIDField(allow_null=True, required=False, default=None)
    output_format = serializers.CharField(required=True)
    message_user_id = serializers.IntegerField(required=False)
    message_ai_id = serializers.CharField(required=False)
    type_data = serializers.CharField(required=False)

class ImagePathSerializer(serializers.Serializer):
    path = serializers.CharField(max_length=255)


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)