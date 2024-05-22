import io
import json
import time
import random
import uuid 
import string
from typing import List
import g4f
from util import TextTran, Settings
from chat.database_utils import save_data_in_db
from fp.fp import FreeProxy
from undetected_chromedriver import Chrome, ChromeOptions
# from g4ff import g4ff0202, g4ff0203, g4ff0204
settings = Settings()
# from g4f import set_cookies

errors_response = [
        "https://static.cloudflareinsights.com/beacon.min.js/",
    "mlc::llm::LLMChatModule::GetFunction",
    "<PHIND_BACKEND_ERROR>",
    "mlc::llm::LLMChatModule"
]

class BaseGenerator:
    def __init__(self, req):
        self.g4f = g4f
        self.valid_request = req
        self.max_attempts = 5
        self.max_retries = 5
        self.completion_id = ''.join(random.choices(string.ascii_letters + string.digits, k=28))
        self.completion_timestamp = int(time.time())
        self.webdriver = None
        self.initialize_request_attributes(req)
        self.errors_response = errors_response

    def initialize_request_attributes(self, req):
        self.model = req.get('model', settings.default_model_text['code'])
        self.stream = req.get('is_stream', False)
        self.provider = req.get('provider', None)
        self.temperature = req.get('temperature', 0.8)
        self.top_p = req.get('top_p', 0.8)
        self.message = req.get('message', [{"role": "user", "content": "Hello"}])
        self.timeout = req.get('timeout', settings.timeout_chat)
        self.proxy = req.get('proxy', settings.default_proxy)
        self.is_tran = req.get('is_tran', False)
        self.is_tran_res = req.get('is_tran_res', False)
        self.lang = req.get('lang', '')
        self.is_web_search = req.get('is_web_search', False)
        self.image =  req.get('image_url', None)# #req.get('image_uri', None)
        self.conversation_id = req.get('conversation_id', str(uuid.uuid4()))

    def gen_text(self):
        if self.stream:
            
            res = self.create_stream_response()
        else:
            res = self.create_non_stream_response()
        return res



    def prepare_params(self):
        params = {
            "model": self.model,
            "messages": self.message,
            "stream": self.stream,
        }
        # if self.model == 'llama2-70b':
        #     self.g4f = g4ff0204
        #     params["provider"] = 'Llama2'
        if self.model == 'gpt-4':
            self.g4f = g4f
            params["provider"] = 'Bing'
            params['web_search'] = False
            # proxy = FreeProxy().get()
            # print("proxy", proxy)
            # params["proxy"] = proxy
            # self.g4f = g4ff0204
            # set_cookies(".bing", {
            #             "_U": "1YauOWqa4RHPd6MqN_F5dG372dSLMu5bwxyGQFmlYU4Q3vG0OdvH1DV7KB8BBs-d0YjHTvLNHswj-NT00mb4-nv8k7DiAhj1D0Eq4QZ7F86KzJmf4GY9rfDIS2Lk15QgQkN2hJ3CYGHWaI_Pxwwv1TL4AJBJRrEXug8aqgGX688NBpuX48oBCi3iJPySdM9NLe9t3ICF2c1jqHpagh9w4fQ"
            #             })
            # options = ChromeOptions()
            # options.add_argument("--incognito")
            # self.webdriver = Chrome(options=options, headless=True, version_main = 120)
            # params["webdriver"] = self.webdriver
            
            if self.is_web_search:
                params["web_search"] = self.is_web_search
                
        if self.image:
            params["image"] =  open(self.image, "rb")
            
        # if self.model == 'mixtral-8x7b':
            # self.g4f = g4ff0204
            # params["provider"] = 'huggingface'
        # if self.model  == 'gemini-pro':
        #     self.g4f = g4ff0204
            # params["provider"] = 'FreeChatgpt'
            
        print("params", params)
        return params

    def create_non_stream_response(self):
        raise NotImplementedError("create_non_stream_response method must be implemented in the subclass")

    def create_stream_response(self):
        raise NotImplementedError("create_stream_response method must be implemented in the subclass")
