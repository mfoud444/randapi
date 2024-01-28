import json
import time
import random
import uuid 
import string
from typing import List
import g4f
from util import TextTran, Settings
from chat.database_utils import save_data_in_db
# from g4ff import g4ff0202, g4ff0203, g4ff0204
from fp.fp import FreeProxy
settings = Settings()
from undetected_chromedriver import Chrome, ChromeOptions
from .BaseGenerator import BaseGenerator

class ChatText(BaseGenerator):
    def __init__(self, req):
        super().__init__(req)
        
    def create_non_stream_response(self):
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

