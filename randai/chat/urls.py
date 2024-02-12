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
router.register(r'api-option', ApiOptionViewSet)
router.register(r'api-keys', ApiKeyViewSet)
router.register(r'api-owner', ApiOwnerViewSet)
router.register(r'lang', LanguageAPIViewSet)
router.register(r'company-ai', CompanyAIAPIViewSet)
router.register(r'provider', ProviderAPIViewSet)
router.register(r'model', ListModelAPIViewSet)
router.register(r'character', CharacterAPIViewSet)
router.register(r'prompt', PromptAPIViewSet)
router.register(r'conversation', ConversationAPIViewSet)
router.register(r'message-user', MessageUserAPIViewSet)
router.register(r'message-ai', MessageAIAPIViewSet)
router.register(r'update-message-ai', MessageAISet)

router.register(r'messages', ListMessagesAPIViewSet)
router.register(r'images', ListImageAIAPIViewSet)
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
    
    
    
        path('tel/start', TelegramServiceView.as_view(), name='tel-start'),
    
    
    
        path('tel/groups', GroupAPIView.as_view(), name='groups'),
          path('tel/keywords', KeyWordAPIView.as_view(), name='keywords'),
           path('tel/verify-code/', CodeVerificationView.as_view(), name='verify_code'),
    
]

