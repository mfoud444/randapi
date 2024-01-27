import json
from pathlib import Path

class Settings:
    TOKAN_LAST = "jUSOLlYPaqpHxBDmX"
    START = "hf_voHpivBBmKCvyThoi"
    TOKAN = START + TOKAN_LAST
    MODEL_API_IMAGE_HUGG = {
        'aesthetic': 'playgroundai/playground-v2-1024px-aesthetic',
        'stable_diffusion_v1_5': 'runwayml/stable-diffusion-v1-5',
        'stabilityai': 'stabilityai/stable-diffusion-xl-base-1.0',
        'compvis': 'CompVis/stable-diffusion-v1-4',
        'SSD-1B':'segmind/SSD-1B'
    }
    UPLOAD_FOLDER_IMAGE = "out/images"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    HOST = "https://randai09078-randdaj.hf.space"
    # HOST = "http://127.0.0.1:8000"
    PORT = "8000"
    IS_TRAN = True
    STATE_CHOICES = [
        ('Running', 'Running'),
        ('Busy', 'Busy'),
        ('Stopped', 'Stopped'),
        ('Unknown', 'Unknown'),
    ]

    TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
         ('research', 'Research'),
    ]
    TYPE_PRICE = [
        ('free', 'Free'),
        ('paide', 'Paide'),
    ]
    default_model_image = {
        'code':'SSD-1B',
        'provider':None,
        'lang':['en'],
        'api_owner':'stabilityai',
    }

    default_model_text ={
        'code':'llama2-70b',
        'provider':None,
        'lang':['en','ar'],
        'api_owner':'stabilityai',
    }
    timeout_chat = 90
    default_proxy = None
    system_message_rand = {}

    def __init__(self):
        self.load_system_message_rand()

    @classmethod
    def load_system_message_rand(cls):
        json_file_path = Path(__file__).resolve().parent / 'system_prompt.json'
        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                cls.system_message_rand = json.load(json_file)
        except FileNotFoundError:
            print(f"Warning: {json_file_path} not found. Using an empty dictionary.")
            cls.system_message_rand = {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {json_file_path}: {e}")
            cls.system_message_rand = {}
