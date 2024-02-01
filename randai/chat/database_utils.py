# database_utils.py
from django.shortcuts import get_object_or_404
from django.utils import timezone
from chat.ModelsAi import ModelAI
from .models import Language
from .Conversation import Conversation
from chat.Messages import MessageUser, MessageAI, TextTranMessage
from .Images import ImageAI, MessageUserImage
from util.Helper import Helper
from django.http import Http404
from util import TextTran
helper = Helper()

def save_data_in_db(valid_request, response, is_image=False):
    try:
        if 'model' not in valid_request:
            raise KeyError("'model' key not found in valid_request")

        model_name = valid_request['model']
        model_instance = get_object_or_404(ModelAI, code=model_name)

        if valid_request['conv'] is None:
            lang_code = valid_request.get('lang', '')
            language_instance = get_object_or_404(Language, code=lang_code)
            conversation_data = {
                'id':valid_request['conversation_id'],
                'user_id': valid_request['user_id'],
                'lang': language_instance,
                'type': valid_request.get('type', 'text'),
                'model': model_instance,
                'title': valid_request['prompt'][:50],
                'is_pin': False,
                'is_favorite': False,
                'is_like': None,
                'created_at': timezone.now(),
                'updated_at': timezone.now(),
            }
            
            conversation = Conversation.objects.create(**conversation_data)
        else:
            conversation = valid_request['conv']
            conversation.updated_at = timezone.now()
            conversation.save()

        if is_image:
            image_paths = response.get('image_paths', [])
            model_instance_image = []
            for image_path in image_paths:
                data = {
                    'image_path': image_path,
                    'model': model_instance,
                    'is_like': None,
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                }
                image_instance = ImageAI.objects.create(**data)
                model_instance_image.append(image_instance)
            if 'parent_message_id' in valid_request and valid_request['parent_message_id']:
                message_user = MessageUserImage.objects.get(id=valid_request['parent_message_id'])
            else:
                message_user_data = {
                    'conversation': conversation,
                    'text': valid_request['prompt'],
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                }
                message_user = MessageUserImage.objects.create(**message_user_data)

            #helper.make_url_image(image.image_path),
            message_user.image_ai.set(model_instance_image)
            return {
                "conversation": {"id": str(conversation.id), "title": conversation.title,  'updated_at':str(conversation.updated_at)},
                "messageUser": {"id": message_user.id},
                "messageAi": [{"id": image.id, "imagePath": image.image_path, "loading": False} for image in
                              model_instance_image],
            }
        else:
            res = response.get('text', '')
            data = {
                'text': response.get('text', ''),
                'model': model_instance,
                'is_like': None,
                'created_at': timezone.now(),
                'updated_at': timezone.now(),
            }
            message_message_ai_text = MessageAI.objects.create(**data)
            if 'parent_message_id' in valid_request and valid_request['parent_message_id']:
                message_user = MessageUser.objects.get(id=valid_request['parent_message_id'])
            else:
                message_user_data = {
                    'conversation': conversation,
                    'text': valid_request['prompt'],
                    'image_path':valid_request.get('image_path', ''),
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                }
                message_user = MessageUser.objects.create(**message_user_data)
            message_user.message_ai.add(message_message_ai_text)
           
            res = response.get('text', '')
            res_translate = response.get('text', '')
            if valid_request.get('is_tran', False):
                    lang_code = valid_request.get('lang', '')
                    text_tran_user = valid_request.get('text_tran_user', '')
                    language_instance = get_object_or_404(Language, code=lang_code)
                    if response.get('text_tran', None):
                        res_translate = response['text_tran']
                        print("None translate Again")
                    else:   
                        res_translate = TextTran().translate_without_code(res, valid_request.get('lang',''))
                    if res_translate:
                        # res = res_translate
                        # print(f"resdd: {res}")
                        text_tran_message_user = TextTranMessage.objects.create(text=text_tran_user, code=language_instance)
                        text_tran_message_ai = TextTranMessage.objects.create(text=res_translate , code=language_instance)
                        message_user.text_tran.add(text_tran_message_user)
                        message_message_ai_text.text_tran.add(text_tran_message_ai)
            text_tran_user_list = list(message_user.text_tran.values())
            text_tran_ai_list = list(message_message_ai_text.text_tran.values())
           
           
            return {
                "conversation": {"id": str(conversation.id), "title": conversation.title, 'updated_at':str(conversation.updated_at)},
                "messageUser": {"id": message_user.id , 'textTranInfo':text_tran_user_list},
                "messageAi": {"id": message_message_ai_text.id, "text": res,'textTranInfo':text_tran_ai_list, "loading": False},
            }

    except Http404 as e:
        print(f"Object not found: {e}")
        return {"error": "Object not found"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An error occurred"}
