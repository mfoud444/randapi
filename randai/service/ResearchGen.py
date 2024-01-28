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

from .research_prompt import get_step_research , get_title
from .BaseGenerator import BaseGenerator
class ResearchGen(BaseGenerator):
    def __init__(self, req):
        super().__init__(req)
        self.step_research = get_step_research(self.lang)

    def create_stream_response(self):
        attempts = 0
        res = {"text": ''}
        completion_data = {
            "conversation": {"id": str(self.conversation_id), "title": ""},
            "messageUser": {"id": 1},
            "messageAi": {"id": 1, "text": "", "loading": True},
        }
        topic = self.valid_request['prompt']
        res["text"] = ""
        generated_results = {}
        params = self.prepare_params()
        params['messages'] = []
        for step, prompt_template in self.step_research.items():
            prompt = prompt_template.format(topic=topic)
            params['messages'] += [{"role": "user", "content": prompt}]
            print("========i am fuck ==========>",step )
            step_result = ""
            while attempts < self.max_attempts:
                try:
                    response = self.g4f.ChatCompletion.create(**params)
                    header_step = self.get_title_step(step)
                    completion_data["messageAi"]["text"] += header_step
                    if response is None:
                        raise ValueError("ChatCompletion.create returned None")
                    for chunk in response:
                        if "https://static.cloudflareinsights.com/beacon.min.js/" in chunk:
                            attempts += 1
                            break
                        step_result += chunk
                        completion_data["messageAi"]["text"] += chunk
                        content = json.dumps(completion_data, separators=(',', ':'))
                        print(completion_data)
                        completion_data["messageAi"]["text"] = ""
                        yield f'{content} \n'

                    
                    generated_results[step] = step_result.strip()
                    params['messages'] += [{"role": "assistant", "content": step_result.strip()}]
                    res["text"] += header_step
                    res["text"] += step_result.strip()  + "\n\n" 
                    break
                except (RuntimeError, Exception) as e:
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
        topic = self.valid_request['prompt']
        generated_results = {}
        params = self.prepare_params()
        params['messages'] = []
        params["stream"] = False
        final_result = "" 

        for step, prompt_template in self.step_research.items():
            prompt = prompt_template.format(topic=topic)
            params['messages'] += [{"role": "user", "content": prompt}]
            retries = 0
            print("========i am fuck ==========>",step )
            while retries < self.max_retries:
                try:
                    response = self.g4f.ChatCompletion.create(**params)
                    if response is not None:
                        generated_results[step] = response
                        params['messages'] += [{"role": "assistant", "content": response}]
                        final_result += self.get_title_step(step)
                        final_result += response.strip()  + "\n\n" 
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
        return {'text': final_result}

    def get_title_step(self, step:str):
        return "\n\n" + "# " + get_title(step.strip(), self.lang).capitalize()  + "\n\n" 