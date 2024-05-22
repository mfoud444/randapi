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
from g4f import ChatCompletion

class ChatText(BaseGenerator):
    def __init__(self, req):
        super().__init__(req)
        
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
                    if any(error_response in response for error_response in self.errors_response):
                        retries += 1
                    else:
                        # Find the index of '<g4f.providers.types.FinishReason'
                        index = response.find('<g4f.providers.types.FinishReason')
                        if index != -1:
                            # Remove everything from the index of '<g4f.providers.types.FinishReason' to the end
                            response = response[:index]
                        break
                else:
                    print("Received None response. Retrying...")
                    retries += 1

            except (RuntimeError, Exception) as e:
                if "FinishReason" in str(e):
                    print("Encountered 'FinishReason' error. Continuing normal process.")
                else:
                    print(f"Error {e}")
                    print(f"Error during generate (Attempt {attempts + 1}/{self.max_attempts})")
                    attempts += 1
                    continue

        
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
                response = ChatCompletion.create(**params)
                # response = self.g4f.ChatCompletion.create(**params)
                if response is None:
                    raise ValueError("ChatCompletion.create returned None")
                for chunk in response:
                    if any(error_response in chunk for error_response in self.errors_response):
                        attempts += 1
                        break
                    res["text"] += chunk
                    completion_data["messageAi"]["text"] = chunk
                    content = json.dumps(completion_data, separators=(',', ':'))
                    # print(completion_data)
                    yield f'{content} \n'

                saved_end_data = save_data_in_db(self.valid_request, res)
                saved_end_data["messageAi"]["text"] = ""
                content = json.dumps(saved_end_data, separators=(',', ':'))
                yield f'{content} \n'
                break
            except (RuntimeError, Exception) as e:
                if "FinishReason" in str(e):
                    print("Encountered 'FinishReason' error. Continuing normal process.")
                    saved_end_data = save_data_in_db(self.valid_request, res)
                    saved_end_data["messageAi"]["text"] = ""
                    content = json.dumps(saved_end_data, separators=(',', ':'))
                    yield f'{content} \n'
                    break
                else:
                    print(f"Error {e}")
                    print(f"Error during generate (Attempt {attempts + 1}/{self.max_attempts})")
                    attempts += 1
                    continue
            finally:
                if self.webdriver:
                    self.webdriver.quit() 

