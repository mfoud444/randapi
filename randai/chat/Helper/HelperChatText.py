import json
import time
import requests
import base64
import random
from PIL import Image
import io
import string
import logging
from typing import List
from g4f import ChatCompletion
from util import TextTran , Settings
import uuid 
from django.shortcuts import get_object_or_404
from chat.models import *
from service import ChatText
from chat.ModelsAi import ModelAISerializer , ModelAI
from chat.Conversation import Conversation
from chat.Messages import MessageUser , ListMessagesSerializer


class HelperChatText:
    def __init__(self, user_req,  is_image=False , is_research = False):
        self.user_req = user_req
        self.validate_req = {}
        self.is_image = is_image
        self.is_research = is_research
        self.settings = Settings(is_emojis=self.user_req.get('is_emojis',True))

    def build_valid_request(self):
        self.initialize_valid_request()
      
        
        
        self.set_model_information()
        self.check_language_support()
        self.set_conversation()
        # self.check_stream()
        self.append_user_message()
        if self.is_image:
            if self.validate_req['text_tran_user'] is None:
                 self.translate()
            # self.validate_req['model'] = 'SSD-1B'
            self.validate_req['type'] = 'image'
        if self.is_research:
            self.validate_req['type'] = 'research'
            
        if self.validate_req['image_path']:
            self.validate_req['image_url'] = self.image_path_to_data_uri(self.validate_req['image_path'])
            # self.validate_req['image_uri'] = self.image_path_to_data_uri(self.validate_req['image_path'])

            
        
            
        return self.validate_req

    def initialize_valid_request(self):
        self.validate_req = {
            'conversation_id': self.user_req.get('conversation_id', str(uuid.uuid4())),
            'user_id': self.user_req['user_id'],
            'model': self.user_req.get('model', ''),
            'is_stream': self.user_req.get('is_stream', False),
            'provider': '',
            'temperature': self.user_req.get('temperature', 0.8),
            'top_p': self.user_req.get('top_p', 0.8),
            'message': [{'role': 'system', 'content': self.settings.system_message_rand.get(self.user_req.get('lang', 'en'),'') }],
            'is_tran': False,
            'lang': self.user_req.get('lang', ''),
            'conv': None,
            'prompt': self.user_req.get('prompt', ''),
            'parent_message_id': self.user_req.get('parent_message_id', ''),
            'text_tran_user':None,
            'is_web_search':self.user_req.get('is_web_search', False),
            'image_path':self.user_req.get('image', ''),
            'image_uri':'',
            'type':'text',
            'is_emojis':self.user_req.get('is_emojis', True),
        }

    def set_conversation(self):
        conversation_id = self.user_req.get('conversation_id')
        if conversation_id is not None:
            existing_conversation = Conversation.objects.filter(id=conversation_id).first()
            if existing_conversation:
                self.validate_req['conv'] = existing_conversation
                if not self.is_image or not self.is_research:
                    self.validate_req['message'] += self.build_message(conversation_id)
        else:
            self.validate_req['conversation_id']  =  str(uuid.uuid4())

    def set_model_information(self):
        model_code = self.user_req.get('model')
        if model_code:
            self.get_valid_model_stream(model_code)
        else:
            self.set_default_model_information()

    def check_language_support(self):
        lang_des = self.user_req.get('lang')
        if 'languages' in self.validate_req and lang_des and lang_des not in self.validate_req['languages']:
            self.validate_req['is_tran'] = True
            self.validate_req['is_stream'] = False

    # def check_stream(self):
    #     is_stream = self.user_req.get('is_stream')
    #     if is_stream is not None:
    #         self.validate_req['is_stream'] = is_stream
    #     else:
    #         self.validate_req['is_stream'] = settings.default_model_text.get('is_stream', False)

    def append_user_message(self):
        if self.validate_req['is_tran']:
            self.validate_req['is_stream'] = False
            max_attempts = 3

            for attempt in range(1, max_attempts + 1):
                try:
                    # Try translating the text
                    self.translate()
                    if self.validate_req['text_tran_user']:
                        print("Translation successful:", self.validate_req['text_tran_user'])
                        self.validate_req['message'] += [{"role": "user", "content": self.validate_req['text_tran_user']}]
                        self.validate_req['message'][0] = {'role': 'system', 'content': self.settings.system_message_rand.get('en', '')}
                        print("self.validate_req['message'][0]", self.validate_req['message'][0])
                        break  # Break out of the loop if translation is successful
                    else:
                        print("Translated text is empty")
                except Exception as e:
                    print(f"Error occurred during translation attempt {attempt}: {e}")

                    if attempt < max_attempts:
                        print("Retrying translation...")
                    else:
                        print("Max attempts reached, setting original text")
                        self.validate_req['message'] += [{"role": "user", "content": self.user_req['prompt']}]
        else:
            self.validate_req['message'] += [{"role": "user", "content": self.user_req['prompt']}]


    def get_valid_model_stream(self, model_code):
        try:
            model_ai_instance = ModelAI.objects.get(pk=model_code)
            model_ai_serializer = ModelAISerializer(model_ai_instance)
            model_ai = model_ai_serializer.data
            if model_ai["is_active"] and model_ai["state"] == "Running":
                self.validate_req.update({
                    "model": model_ai["code"],
                    "is_stream": model_ai["is_stream"],
                    "provider": model_ai["provider"],
                    "languages": model_ai["languages"]
                })
            else:
                self.set_default_model_information()

            print(f"Retrieved ModelAI instance: {model_ai}")
        except ModelAI.DoesNotExist:
            print(f"ModelAI instance with model_code {model_code} not found")
            self.set_default_model_information()

    def set_default_model_information(self):
        default_model = self.settings.default_model_image if self.is_image else self.settings.default_model_text
        self.validate_req.update({
            "model": default_model['code'],
            "provider": default_model['provider'],
            "is_stream": default_model.get('is_stream', False),
            "languages": default_model['lang']
        })
    
    def translate(self):
         self.validate_req['text_tran_user'] = TextTran().translate_without_code(self.user_req['prompt'], 'en')
         
    def build_message(self, conversation_id):
        try:
            message_user_instances = MessageUser.objects.filter(conversation__id=conversation_id)

            if message_user_instances:
                all_messages = []

                for message_user_instance in message_user_instances:
                    serializer = ListMessagesSerializer(message_user_instance)
                    data = serializer.data

                    if self.validate_req.get('is_tran', False) and 'text_tran_info' in data['message_user']:
                        user_message_content = data['message_user']['text_tran_info'][0]['text'] if data['message_user']['text_tran_info'] else ''
                    else:
                        user_message_content = data['message_user'].get('text', '')

                    user_message = {
                        'role': 'user',
                        'content': user_message_content
                    }

                    if 'parent_message_id' in self.validate_req and self.validate_req['parent_message_id'] == data['message_user']['id']:
                        break

                    assistant_messages = [{
                        'role': 'assistant',
                        'content': msg['text'] if 'text' in msg else ''
                    } for msg in data['message_ai']]

                    all_messages.append(user_message)
                    all_messages.extend(assistant_messages)

                return all_messages

            else:
                return [{'error': 'No messages found for the given conversation_id'}]

        except Exception as e:
            return [{'error': str(e)}]

        
        import base64

    

    def image_path_to_data_uri(self, image_path):
        try:
            supabase_url_file = 'https://fvpmikdmeystnnxnloqe.supabase.co/storage/v1/object/public/chat-text/' + image_path
            response = requests.get(supabase_url_file)

            if response.status_code == 200:
                with open('image.jpg', 'wb') as f:
                    f.write(response.content)
                print('Image downloaded successfully')
                return "/home/mohammed/Projects/backendrand/randapi/randai/image.jpg"
                
            else:
                print('Failed to download image')
        #     print(supabase_url_file)
        #     response = requests.get(supabase_url_file)
        #     if response.status_code == 200:
        #         image_data = response.content
        #         base64_encoded_image = base64.b64encode(image_data).decode("utf-8")
        #         file_extension = image_path.split(".")[-1]
        #         image_format = "jpeg" if file_extension.lower() == "jpg" else file_extension.lower()
        #         data_uri = f"data:image/{image_format};base64,{base64_encoded_image}"
        #         return data_uri
        #     else:
        #         print(f"Failed to fetch image. Status code: {response.status_code}")
        #         return None
        except Exception as e:
            print(f"Error converting image to data URI: {e}")
            return None
