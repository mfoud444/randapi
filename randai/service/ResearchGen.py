import json
import time
import random
import uuid 
import string
import concurrent.futures
from typing import List
import g4f
from util import TextTran, Settings
from chat.database_utils import save_data_in_db
# from g4ff import g4ff0202, g4ff0203, g4ff0204
from fp.fp import FreeProxy
settings = Settings()
import asyncio
from undetected_chromedriver import Chrome, ChromeOptions
from util import TextTran
from .research_prompt import get_step_research , get_title
from .BaseGenerator import BaseGenerator
class ResearchGen(BaseGenerator):
    def __init__(self, req):
        super().__init__(req)
        
        if self.valid_request['is_tran']:
          
            self.topic = self.valid_request['text_tran_user']
            
            self.step_research = get_step_research('en')
        else:
          
            self.topic = self.valid_request['prompt']
            self.step_research = get_step_research(self.lang)
        
    def get_title_step(self, step: str, lang=None):
        if lang is None:
            lang = self.lang
        return "\n\n" + "# " + get_title(step.strip(), lang).capitalize() + "\n\n"
    
    def create_stream_response(self):
        
        res = {"text": ''}
        completion_data = {
            "conversation": {"id": str(self.conversation_id), "title": ""},
            "messageUser": {"id": 1},
            "messageAi": {"id": 1, "text": "", "loading": True},
        }
        
        res["text"] = ""
        generated_results = {}
        params = self.prepare_params()
        params['messages'] = []
        for step, prompt_template in self.step_research.items():
            attempts = 0
            prompt = prompt_template.format(topic=self.topic)
            params['messages'] += [{"role": "user", "content": prompt}]
            
            step_result = ""
            while attempts < self.max_attempts:
                try:
                    print("attemp", attempts)
                    response =self.g4f.ChatCompletion.create(**params)
                    # print("response",response)
                    header_step = self.get_title_step(step)
                    completion_data["messageAi"]["text"] += header_step
                    if response is not None and response:
                        print(response)
                        for chunk in response:
                            if any(error_response in chunk for error_response in self.errors_response):
                                print("annny error")
                                print(f"Received None response for step {step}. Retrying...")
                                attempts += 1
                                break
                            else:
                                try:
                                    decoded_chunk = chunk
                                    step_result += decoded_chunk
                                    completion_data["messageAi"]["text"] += decoded_chunk
                                    content = json.dumps(completion_data, separators=(',', ':'))
                                    # print("completion_data",step)
                                    completion_data["messageAi"]["text"] = ""
                                    yield f'{content} \n'
                                except UnicodeDecodeError as decode_error:
                                    print(f"UnicodeDecodeError: {decode_error}")
                                    continue

                        # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",response)
                        generated_results[step] = step_result.strip()
                        params['messages'] += [{"role": "assistant", "content": step_result.strip()}]
                        res["text"] += header_step
                        res["text"] += step_result.strip()  + "\n\n" 
                        break
                    else:
                        print(f"Received None response for step {step}. Retrying...")
                        attempts += 1
                        continue
                except (RuntimeError, Exception) as e:
                    print("errpr rrr")
                    print(f"Error {e}")
                    print(f"Error during generate (Attempt {attempts + 1}/{self.max_attempts})")
                    attempts += 1
                    continue
                finally:
                    if self.webdriver:
                        self.webdriver.quit() 
     
        saved_end_data = save_data_in_db(self.valid_request, res)
        saved_end_data["messageAi"]["text"] = ""
        content = json.dumps(saved_end_data, separators=(',', ':'))
        yield f'{content} \n'


    def create_non_stream_response(self):
        generated_results = {}
        completion_data = {
            "conversation": {"id": str(self.conversation_id), "title": ""},
            "messageUser": {"id": 1},
            "messageAi": {"id": 1, "text": "", "loading": True},
        }
        params = self.prepare_params()
        params['messages'] = []
        params["stream"] = False
        text_results = "" 
        tran_text_results = ""
        lang = self.lang
        
        if self.is_tran:
            lang = 'en'
            

        for step, prompt_template in self.step_research.items():
            if self.is_tran:
                header_step = self.get_title_step(step, self.lang)
                header_step_tran = self.get_title_step(step, 'en')
            else:
                header_step = self.get_title_step(step)
                header_step_tran = self.get_title_step(step)
                
            print(self.topic) 
            prompt = prompt_template.format(topic=self.topic)
            print(prompt)
            params['messages'] += [{"role": "user", "content": prompt}]
            retries = 0
            print("========i am fuck ==========>",step )
            
            completion_data["messageAi"]["text"] += header_step
            content = json.dumps(completion_data, separators=(',', ':'))
            yield f'{content} \n'
            while retries < self.max_retries:
                try:
                    response = self.g4f.ChatCompletion.create(**params)
                    print(response)
                    if response is not None and response != '':
                        if any(error_response in response for error_response in self.errors_response):
                            retries += 1
                            break
                        else:
                            generated_results[step] = response
                            params['messages'] += [{"role": "assistant", "content": response}]
                            
                            completion_data["messageAi"]["text"] = response
                            
                            text_results += header_step_tran
                            text_results += response.strip()  + "\n\n"
                            if self.is_tran:
                                response_tran  = TextTran().translate_without_code(response, self.lang).strip() + "\n\n"
                                completion_data["messageAi"]["text"] = response_tran
                                tran_text_results += header_step
                                tran_text_results += response_tran
                                # print("tran_text_results", tran_text_results)
                            content = json.dumps(completion_data, separators=(',', ':'))
                            yield f'{content} \n'
                            completion_data["messageAi"]["text"] = ""
                            break 
                    else:
                        print(f"Received None response for step {step}. Retrying...")
                        retries += 1

                except (RuntimeError, Exception) as e:
                    print(f"Error during generate for step {step}: {str(e)}")
                    if retries < self.max_retries - 1:
                        print(f"Retrying... Attempt {retries + 2}/{self.max_retries}")
                        retries += 1
                    else:
                        raise  
        saved_end_data = save_data_in_db(self.valid_request, {'text': text_results , 'text_tran':tran_text_results})
        completion_data["messageUser"]["id"] = saved_end_data["messageUser"]["id"]
        completion_data["messageAi"]["id"] = saved_end_data["messageAi"]["id"]
        completion_data["messageAi"]["text"] = ""
        # saved_end_data["messageAi"]["text"] = ""
        content = json.dumps(completion_data, separators=(',', ':'))
        yield f'{content} \n'

