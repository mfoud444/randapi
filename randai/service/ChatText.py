import json
import time
import random
import uuid 
import string
from typing import List
import g4f
from util import TextTran, Settings
from chat.database_utils import save_data_in_db
from g4ff import g4ff0202, g4ff0203, g4ff0204
from fp.fp import FreeProxy
settings = Settings()
import g4f
from undetected_chromedriver import Chrome, ChromeOptions



class ChatText:
    def __init__(self, req):
        self.g4f = g4f
        self.valid_request = req
        self.max_attempts = 5
        self.max_retries = 3
        self.completion_id = ''.join(random.choices(string.ascii_letters + string.digits, k=28))
        self.completion_timestamp = int(time.time())
        self.webdriver = None 
        self.initialize_request_attributes(req)
        

    def initialize_request_attributes(self, req):
        self.model = req.get('model', settings.default_model_text['code'])
        self.stream = req.get('is_stream', False)
        self.provider = req.get('provider', None)
        self.temperature = req.get('temperature', 0.8)
        self.top_p = req.get('top_p', 0.8)
        self.message = req.get('message', [{"role": "user", "content": "Hello"}])
        self.timeout = req.get('timeout', settings.timeout_chat)
        self.proxy = req.get('proxy', settings.default_proxy)
        self.is_tran_req = req.get('is_tran_req', False)
        self.is_tran_res = req.get('is_tran_res', False)
        self.lang_des = req.get('lang_des', '')
        self.is_web_search = req.get('is_web_search', False)
        self.image = req.get('image_uri', None)
        self.conversation_id = req.get('conversation_id', str(uuid.uuid4()))

    def gen_text(self):
        if self.stream:
            res = self.create_stream_response()
        else:
            res = self.create_non_stream_response()
        return res

    def generate_response(self):
        retries = 0
        while retries < self.max_retries:
            try:
                params = self.prepare_params()
                response = self.g4f.ChatCompletion.create(**params)
                if response is not None:
                    return response
                else:
                    print("Received None response. Retrying...")
                    retries += 1

            except (RuntimeError, Exception) as e:
                print(f"Error during generate:")
                if retries < self.max_retries - 1:
                    print(f"Retrying... Attempt {retries + 2}/{self.max_retries}")
                    retries += 1
                else:
                    raise

    def prepare_params(self):
        params = {
            "model": self.model,
            "messages": self.message,
            "stream": self.stream,
        }
        # if self.model == 'llama2-70b':
        #     params["provider"] = 'Llama2'
        if self.model == 'gpt-4':
            params["provider"] = 'Bing'
            # proxy = FreeProxy().get()
            # print("proxy", proxy)
            # params["proxy"] = proxy
            self.g4f = g4f
            options = ChromeOptions()
            options.add_argument("--incognito")
            self.webdriver = Chrome(options=options, headless=True, version_main = 120)
            params["webdriver"] = self.webdriver
            
            if self.is_web_search:
                params["web_search"] = self.is_web_search
                
        if self.image:
            params["image"] = self.image
            
        # if self.model == 'mixtral-8x7b':
        #     params["provider"] = 'huggingface'
        print("params", params)
        return params

    def create_non_stream_response(self):
        response = self.generate_response()
        return {'text': response}

    def create_stream_response(self):
        attempts = 0
        res = {"text": ''}
        completion_data = {
            "conversation": {"id": str(self.conversation_id), "title": ""},
            "messageUser": {"id": 1},
            "messageAi": {"id": 1, "text": "", "loading": True},
        }
        while attempts < self.max_attempts:
            try:
                params = self.prepare_params()
                response = self.g4f.ChatCompletion.create(**params)
                if response is None:
                    raise ValueError("ChatCompletion.create returned None")
                for chunk in response:
                    if "https://static.cloudflareinsights.com/beacon.min.js/" in chunk:
                        attempts += 1
                        break
                    res["text"] += chunk
                    completion_data["messageAi"]["text"] = chunk
                    content = json.dumps(completion_data, separators=(',', ':'))
                    print(completion_data)
                    yield f'{content} \n'

                saved_end_data = save_data_in_db(self.valid_request, res)
                saved_end_data["messageAi"]["text"] = ""
                content = json.dumps(saved_end_data, separators=(',', ':'))
                yield f'{content} \n'
                break
            except (RuntimeError, Exception) as e:
                print(f"Error {e}")
                print(f"Error during generate (Attempt {attempts + 1}/{self.max_attempts})")
                attempts += 1
                continue
            finally:
                if self.webdriver:
                    self.webdriver.quit() 
