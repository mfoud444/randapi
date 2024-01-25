# myapp/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import RequestAborted
from rest_framework.views import APIView
from django.http import FileResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
from .database_utils import save_data_in_db
from .serializers import *
from rest_framework import viewsets
from .Helper.HelperChatText import HelperChatText
from .Conversation import Conversation
from service import ChatText, ImageGenerator
from django.http import StreamingHttpResponse, HttpResponse
from util import TextTran, Settings, PandocConverter
from chat.ModelsAi import ModelAI, ModelAISerializer
from chat.Messages import (
    MessageUser,
    MessageAI,
    MessageUserSerializer,
    MessageAISerializer,
)

settings = Settings()
import os


def validate_required_fields(request, required_fields):
    missing_fields = [
        field for field in required_fields if request.data.get(field) is None
    ]
    if missing_fields:
        field_list = ", ".join(missing_fields)
        return Response(
            {"error": f"The following fields are required: {field_list}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


class LanguageAPIViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        print(
            "serializer.errors"
        )  # Print validation errors to the console for debugging

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CompanyAIAPIViewSet(viewsets.ModelViewSet):
    queryset = CompanyAI.objects.all()
    serializer_class = CompanyAISerializer


class ProviderAPIViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ApiOwnerViewSet(viewsets.ModelViewSet):
    queryset = ApiOwner.objects.all()
    serializer_class = ApiOwnerSerializer


class ApiOptionViewSet(viewsets.ModelViewSet):
    queryset = ApiOption.objects.all()
    serializer_class = ApiOptionSerializer


class ApiKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer


class ModelAPIViewSet(viewsets.ModelViewSet):
    queryset = ModelAI.objects.all()
    serializer_class = ModelAISerializer


class CharacterAPIViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class PromptAPIViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class MessageUserAPIViewSet(viewsets.ModelViewSet):
    queryset = MessageUser.objects.all()
    serializer_class = MessageUserSerializer


class MessageAIAPIViewSet(viewsets.ModelViewSet):
    queryset = MessageAI.objects.all()
    serializer_class = MessageAISerializer


class ChatAPIView(APIView):
    def handle_request(self, request, is_image):
        try:
            data = request.data
            serializer = ChatTextSerializer(data=data)
            print(request.data)

            if serializer.is_valid():
                valid_request = serializer.validated_data
                print(valid_request)
                if is_image:
                    print("serializer.validated_data")
                    helper_instance = HelperChatText(serializer.validated_data, True)
                    valid_request = helper_instance.build_valid_request()
                    print("valid_request", valid_request)
                    object_chat = ImageGenerator(valid_request)
                    response = object_chat.gen_image()
                    if response["image_paths"]:
                        print("response", response)
                        res = save_data_in_db(valid_request, response, is_image)
                        print("res", res)
                        return Response(res, status=status.HTTP_200_OK)
                    else:
                        print(f"Error processing image request:")
                        return Response(
                            {"error": "Error processing image request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                else:
                    helper_instance = HelperChatText(serializer.validated_data)
                    valid_request = helper_instance.build_valid_request()
                    object_chat = ChatText(valid_request)
                    print("valid_request", valid_request)

                    if valid_request.get("is_stream", False):
                        return StreamingHttpResponse(
                            object_chat.create_stream_response(),
                            content_type="text/event-stream",
                        )
                    else:
                        response = object_chat.gen_text()
                        print("valid_request", valid_request)
                        print("response", response)
                        res = save_data_in_db(valid_request, response)
                        return Response(res, status=status.HTTP_200_OK)

            else:
                print("serializer.errors", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RequestAborted:
            # Handle the aborted request
            return Response(
                {"detail": "Request aborted by the user"},
                status=status.HTTP_499_CLIENT_CLOSED_REQUEST,
            )
        except Exception as e:
            print(str(e))
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatTextAPIView(ChatAPIView):
    def post(self, request, *args, **kwargs):
        return self.handle_request(request, is_image=False)


class ChatImageAPIView(ChatAPIView):
    def post(self, request, *args, **kwargs):
        print("serializer.validated_data")
        return self.handle_request(request, is_image=True)


class GetImageView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            serializer = ImagePathSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            path = serializer.validated_data["path"]
            path = os.path.normpath(path)
            print(path)
            if not os.path.exists(path) or not os.path.isfile(path):
                return Response(
                    {"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND
                )
            with open(path, "rb") as image_file:
                return HttpResponse(image_file.read(), content_type="image/png")
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from .Messages import ListMessagesSerializer


class DocumentDownloadView(APIView):
    def build_message(self, data):
        try:
            print("data", data)
            type_data = data.get("type_data", "")
            conversation_id = data.get("conversation_id", "")
            try:
                conversation = Conversation.objects.filter(id=conversation_id)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
            print(conversation_id, type_data)
            if type_data == "conversation":
                message_user_instances = MessageUser.objects.filter(conversation__id=conversation_id)

                if message_user_instances:
                    all_messages = []

                    for message_user_instance in message_user_instances:
                        serializer = ListMessagesSerializer(message_user_instance)
                        data = serializer.data

                        user_message = (
                            data["message_user"]["text"]
                            if "message_user" in data
                            else ""
                        )
                        user_message += "\n"
                        assistant_messages = []
                        for i, msg in enumerate(data["message_ai"]):
                            text = msg.get("text", "")
                            formatted_msg = (
                                f"Answer-{i}\n" if i > 0 else ""
                            ) + f"\n{text}\n"
                            assistant_messages.append(formatted_msg)

                        all_messages.append(user_message)
                        all_messages.extend(assistant_messages)

                 
                    return "\n".join(all_messages)
            elif type_data == "chat":
                message_user_id = data.get("message_user_id", "")
                message_ai_id = data.get("message_ai_id", 0)
                print("hhhhhhhhhh")
                print("message_ai_id", message_ai_id)
                message_user_instance = MessageUser.objects.filter(id=message_user_id, conversation__id=conversation_id).first()
                if message_user_instance:
                    serializer = ListMessagesSerializer(message_user_instance)
                    data = serializer.data
                    user_message = (data["message_user"]["text"] if "message_user" in data else "")
                    user_message += "\n"
                    assistant_message = ""
                    print("data['message_ai']", data["message_ai"])
                    for i, msg in enumerate(data["message_ai"]):
                        id = msg.get("id", "")
                        print("id", id)
                        if message_ai_id == id:
                            assistant_message =msg.get("text", "")
                    return f"{user_message}\n{assistant_message}"
            else:
                return "No messages found for the given conversation_id"

        except Exception as e:
            return str(e)

    def get(self, request, *args, **kwargs):
        try:
            serializer = DocumentclassSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            text_mt = self.build_message(serializer.validated_data)
            input_text = f"{text_mt}"
            output_format = serializer.validated_data.get("output_format", "").lower()
            if output_format == "docx":
                output_file = "output.docx"
                options = ["--to=docx"]
            elif output_format == "pptx":
                output_file = "output.pptx"
                options = ["--to=pptx"]
            else:
                output_file = "output.pdf"
                options = [
                    "--pdf-engine=xelatex",
                    "--variable=geometry:margin=1in",
                    "--template=/usr/share/pandoc/templates/eisvogel.latex",
                    "--variable=mainfont:Amiri",
              
                 "--variable=dir:rtl",
                ]
            #    "--variable=lang:ar",
            #   
            pandoc_converter = PandocConverter(input_text, output_file, options)
            pandoc_converter.convert()
            file_path = os.path.abspath(output_file)
            response = FileResponse(open(file_path, "rb"))
            response["Content-Disposition"] = f'attachment; filename="{output_file}"'
            return response
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
