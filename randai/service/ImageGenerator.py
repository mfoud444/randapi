import os
import io
import concurrent.futures
import requests
from PIL import Image
from util.Settings import Settings
from util.Helper import Helper
from .ImageGen.SSD1 import SSD1
from mysupabase import supabase

class ImageGenerator:
    def __init__(self, req):
        self.req = req
        self.settings = Settings()
        self.helper = Helper()

    def generate_images(self, models, prompt_func):
        prompt = self.req['text_tran_user']
        images_list = []

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.process_model, models, [prompt]*len(models), [images_list]*len(models), [prompt_func]*len(models))
        except Exception as e:
            print(f"Error: {e}")

        return {"image_paths": images_list}

    def gen_image_bing(self):
        return self.generate_images([self.req['model'], self.req['model']], self.prompt_bing)

    def gen_image(self):
        return self.generate_images([self.req['model']] * 4, self.prompt_model)

    def gen_image_huggface(self):
        return self.generate_images([self.req['model'], self.req['model']], self.prompt_model)

    def prompt_model(self, model, prompt, images_list):
        try:
            image = self.make_my_request(prompt, model)
            if image:
                images_list.append(image)
        except Exception as e:
            print(f"Error processing model: {e}")

    def prompt_bing(self, model, prompt, images_list):
        print('hhh', self.req['text_tran_user'])
        try:
            # Uncomment the following lines when ImageTextGenerator is available
            # image_text_generator = ImageTextGenerator(prompt)
            # results = image_text_generator.generate_images_text()
            # images_list.extend(results[0])
            pass
        except Exception as e:
            print(f"Error lo: {e}")

    def process_model(self, model, prompt, images_list, prompt_func):
        prompt_func(model, prompt, images_list)

    def make_my_request(self, prompt, model):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_bytes = SSD1(prompt).gen_image()
        image_name = self.helper.generate_random_filename_image()
        image_path = os.path.join(script_dir, image_name)
        try:
            self.save_image(image_bytes, image_path)
            image_path = self.save_image_supabase(image_path, image_name)
            return image_path
        except Exception as e:
            print(f"Error: {e}")
            print(f"Image Bytes: {image_bytes[:20]}")
            return ''

    def save_image_supabase(self, filepath, image_name):
        try:
            if filepath is None:
                print("Error: Filepath is None")
                return None

            with open(filepath, 'rb') as f:
                response = supabase.storage.from_("ChatImage").upload(file=f, path=image_name)

            print(response.json())
            response = response.json()
            public_url = response['Key']
            print(f"Image uploaded to Supabase: {public_url}")
            return public_url
        except Exception as e:
            print(f"Error saving image to Supabase: {e}")
            return None

    def save_image(self, image_bytes, image_path):
        image = Image.open(io.BytesIO(image_bytes))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        watermark_path = os.path.join(script_dir, "logo.png")
        watermark = Image.open(watermark_path)
        watermark = watermark.resize((50, 50))
        image.paste(watermark, (10, image.height - watermark.height - 10))
        image.save(image_path)










# import json
# import time
# import random
# import string
# import requests
# import io
# import os
# import logging
# from PIL import Image, ImageDraw
# from util.Settings import Settings
# from util.Helper import Helper
# from util import TextTran
# import concurrent.futures
# # from .gpt4free003 import ImageTextGenerator
# from .ImageGen.SSD1 import SSD1
# from mysupabase import supabase
# import base64

# class ImageGenerator:
#     def __init__(self, req):
#         self.req = req
#         self.settings = Settings()
#         self.helper = Helper()


#     def gen_image_bing(self):
#         print('hhh', self.req['text_tran_user'])
#         prompt = self.req['text_tran_user']
#         models = [self.req['model'], self.req['model']] if self.req['model'] else []
#         images_list = []
#         try:
#             image_text_generator = ImageTextGenerator(prompt)
#             results = image_text_generator.generate_images_text()
#             print("results", results)
#             for result in results:
#                 print("result", result)
#             images_list = results[0]
#         except Exception as e:
#             print(f"Error lo: {e}")
#         return {"image_paths":images_list}
    
#     def gen_image(self):
#         prompt = self.req['text_tran_user']
#         models = [self.req['model'], self.req['model'], self.req['model'], self.req['model']] if self.req['model'] else []
#         images_list = []
#         try:
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 executor.map(self.process_model, models, [prompt]*len(models), [images_list]*len(models))
#         except Exception as e:
#             print(f"Error lo: {e}")
#         return {"image_paths":images_list}
    
#     def gen_image_huggface(self):
#         print('hhh', self.req['text_tran_user'])
#         prompt = self.req['text_tran_user']
#         # models = [self.req['model'], 'stabilityai',  'aesthetic',  'compvis', 'stable_diffusion_v1_5'] if self.req['model'] else []
#         models = [self.req['model'], self.req['model']] if self.req['model'] else []
#         images_list = []
#         try:
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 executor.map(self.process_model, models, [prompt]*len(models), [images_list]*len(models))
#         except Exception as e:
#             print(f"Error lo: {e}")
#         return {"image_paths":images_list}


#     def process_model(self, model: str, prompt: str, images_list: list):
#         try:
#             image = self.make_my_request(prompt, model)
#             if image:
#                 images_list.append(image)
#         except Exception as e:
#             print(f"Error processing model: {e}")

#     def make_my_request(self, prompt: str, model: str) -> str:
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         image_bytes = SSD1(prompt).gen_image()
#         image_name = self.helper.generate_random_filename_image()
#         image_path = os.path.join(script_dir,image_name)
#         try:
#             self.save_image(image_bytes, image_path)
#             image_path = self.save_image_supabase(image_path, image_name)
#             return image_path
#         except Exception as e:
#             print(f"Error: {e}")
#             print(f"Image Bytes: {image_bytes[:20]}")
#             return ''
        
#     def make_request(self, prompt: str, model: str) -> str:
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         url = self.helper.get_url_model_api(model)
#         headers = self.helper.get_header_api()
#         image_name = self.helper.generate_random_filename_image()
#         image_path = os.path.join(script_dir, image_name)
#         image_bytes = self.query_model_api(prompt, model, url, headers)
#         try:
#             image_path = self.save_image(image_bytes, image_path)
#             return image_path
#         except Exception as e:
#             print(f"Error: {e}")
#             print(f"Image Bytes: {image_bytes[:20]}")
#             return ''

#     def query_model_api(self, prompt: str, model: str, url: str, headers: dict) -> bytes:
#         payload = {
#             "inputs": prompt,}
#         response = requests.post(url, headers=headers, json=payload)
#         return response.content
    
#     def save_image_supabase(self, filepath: str, image_name:str):
#         try:
#             if filepath is None:
#                 print("Error: Filepath is None")
#                 return None

#             with open(filepath, 'rb') as f:
#                 response = supabase.storage.from_("ChatImage").upload(file=f,path=image_name)
#             print(response.json())
#             response = response.json()
#             # if response['error']:
#             #     print(f"Error uploading image to Supabase: {response['error']}")
#             #     return None

#             public_url = response['Key']
#             print(f"Image uploaded to Supabase: {public_url}")
#             return public_url

#         except Exception as e:
#             print(f"Error saving image to Supabase: {e}")
#             return None

            
        
        
#     def save_image(self, image_bytes: bytes, image_path: str):
#         image = Image.open(io.BytesIO(image_bytes))
#         script_dir = os.path.dirname(os.path.abspath(__file__)) 
#         watermark_path = os.path.join(script_dir, "logo.png")
#         watermark = Image.open(watermark_path)
#         watermark = watermark.resize((50, 50))
#         image.paste(watermark, (10, image.height - watermark.height - 10))
#         image.save(image_path)

#     def get_info_req(self, prompt):
#         url = "https://api.segmind.com/v1/ssd-1b"
#         api_key = 'SG_ce4b5c42de388f4c'
#         data = {
#             "prompt": prompt,
#             "negative_prompt": "scary, cartoon, painting",
#             "samples": 1,
#             "scheduler": "UniPC",
#             "num_inference_steps": 25,
#             "guidance_scale": 9,
#             "seed": 36446545871,
#             "img_width": 1024,
#             "img_height": 1024,

#         }
#         response = requests.post(url, json=data, headers={'x-api-key': api_key})
#         if response.status_code == 200:
#             print("response.json()",response)
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#             return None
#         return response


