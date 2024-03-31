# myapp/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import *
from .Conversation import ConversationAPIViewSet
from .Messages import ListMessagesAPIViewSet,  MessageAISet
from .Images import  ListImageAIAPIViewSet
from .ModelsAi import  ListModelAPIViewSet 
from .Conversation import delete_conversation

router = routers.DefaultRouter()
router.register(r'api-option', ApiOptionViewSet, basename='api-option')
router.register(r'api-keys', ApiKeyViewSet, basename='api-keys')
router.register(r'api-owner', ApiOwnerViewSet, basename='api-owner')
router.register(r'lang', LanguageAPIViewSet, basename='lang')
router.register(r'company-ai', CompanyAIAPIViewSet, basename='company-ai')
router.register(r'provider', ProviderAPIViewSet, basename='provider')
router.register(r'model', ListModelAPIViewSet, basename='model')
router.register(r'character', CharacterAPIViewSet, basename='character')
router.register(r'prompt', PromptAPIViewSet, basename='prompt')
router.register(r'conversation', ConversationAPIViewSet, basename='conversation')
router.register(r'message-user', MessageUserAPIViewSet, basename='message-user')
router.register(r'message-ai', MessageAIAPIViewSet, basename='message-ai')
router.register(r'update-message-ai', MessageAISet, basename='update-message-ai')
router.register(r'messages', ListMessagesAPIViewSet, basename='messages')
router.register(r'images', ListImageAIAPIViewSet, basename='images')
urlpatterns = [
    path('', include(router.urls)),
    path('chat/text', ChatTextAPIView.as_view(), name='chat-text'),
    # path('models/', ListModelAIAPIView.as_view(), name='list-models'),
    # path('messages/', ListMessagesAPIViewSet.as_view(), name='messages'),
    path('chat/image', ChatImageAPIView.as_view(), name='chat-image'),
     path('chat/research', ChatResearchAPIView.as_view(), name='chat-research'),
    path('get-image/', GetImageView.as_view(), name='get-image'),
    path('doc/file/', DocumentDownloadView.as_view(), name='file'),
    path('delete-conversation/<uuid:user_id>/<str:type>/', delete_conversation,
         name='delete_conversation'),
    path('translate/', translate_text, name='translate-text'),
    
    
    
     
    
]

