from rest_framework import serializers
from chat.models import *
from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response
from util import  Settings
from chat.serializers import CompanyAISerializer , ApiOwnerSerializer
settings = Settings()
class ModelAI(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    provider = models.ManyToManyField(Provider, blank=True)
    company_ai_id = models.ForeignKey(CompanyAI, on_delete=models.CASCADE)
    api_owner_id = models.ForeignKey(ApiOwner, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    type_service = models.CharField(max_length=10, choices=settings.TYPE_CHOICES, default='text')
    languages = models.ManyToManyField(Language, blank=True)
    is_active = models.BooleanField()
    is_stream = models.BooleanField()
    is_web_search = models.BooleanField(default=False)
    is_allow_image = models.BooleanField(default=False)
    state = models.CharField(max_length=255, choices=settings.STATE_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ModelAISerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelAI
        fields = '__all__'



class ListModelsSerializer(serializers.ModelSerializer):
    company_ai = CompanyAISerializer(source='company_ai_id', read_only=True)
    api_owner =  ApiOwnerSerializer(source='api_owner_id', read_only=True)
    class Meta:
        model = ModelAI
        fields = '__all__'


class ListModelAPIViewSet(viewsets.ModelViewSet):
    queryset = ModelAI.objects.all()
    serializer_class = ListModelsSerializer
    def get_queryset(self):
        is_active = self.request.query_params.get('is_active')
        if is_active:
            queryset = ModelAI.objects.filter(is_active=is_active)
        else:
            queryset = ModelAI.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            return Response(data, status=200)
        except Exception as e:
            return Response(str(e), status=500)





# class ListModelAIAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             print("request.query_params", request.query_params)
#             filters = {
#                 "code": request.query_params.get("code"),
#                 "provider__id": request.query_params.get("provider_id"),
#                 "company_ai_id": request.query_params.get("company_ai_id"),
#                 "api_owner__id": request.query_params.get("api_owner_id"),
#                 "type_service": request.query_params.get("type_service"),
#                 "is_active": request.query_params.get("is_active"),
#                 "is_stream": request.query_params.get("is_stream"),
#                 "state": request.query_params.get("state"),
#             }
#             filters = {
#                 key: value for key, value in filters.items() if value is not None
#             }
#
#             queryset = ModelAI.objects.filter(**filters)
#             serializer = ModelAISerializer(queryset, many=True)
#
#             # Fetch data from CompanyAI based on company_ai_id
#             company_ai_ids = [item["company_ai_id"] for item in serializer.data]
#             company_ai_data = CompanyAI.objects.filter(id__in=company_ai_ids)
#             company_ai_serializer = CompanyAISerializer(company_ai_data, many=True)
#
#             # Create a dictionary to store CompanyAI data
#             company_ai_dict = {item["id"]: item for item in company_ai_serializer.data}
#
#             # Merge data from ModelAI and CompanyAI serializers
#             for item in serializer.data:
#                 company_ai_item = company_ai_dict.get(item["company_ai_id"])
#                 if company_ai_item:
#                     item["company_ai"] = company_ai_item
#
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             # Handle exceptions and return an error response if necessary
#             response_data = {
#                 "data": None,
#                 "message": str(e),  # You can customize the error message
#                 "status": "error",
#             }
#
#             return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)