import os
import io
import time
import concurrent.futures
import requests
from PIL import Image
from util.Settings import Settings
from util.Helper import Helper
from .ImageGen.SSD1 import SSD1
from mysupabase import supabase
from urllib.parse import urlparse
from g4ff import g4ff0202, g4ff0203, ImageTextGenerator, ImageTextGenerator4


class ImageGenerator:
    def __init__(self, req):
        self.req = req
        self.settings = Settings()
        self.helper = Helper()
        self.script_dir = os.path.abspath("out/images")

    def gen_image(self, type="huggface"):
        image_functions = {
            "bing": self.gen_image_bing,
            "huggface_endpoint": self.gen_image_huggface_endpoint,
            "huggface": self.gen_image_huggface,
        }
        if type in image_functions:
            return image_functions[type]()
        else:

            raise ValueError(f"Unsupported image type: {type}")

    def process_model(self, model, prompt, images_list, prompt_func):
        prompt_func(model, prompt, images_list)

    ## huggface

    def gen_image_huggface(self):
        prompt = self.req["text_tran_user"]
        images_list = []
        models = ["SSD-1B", "SSD-1B", "SSD-1B", "SSD-1B"]
        # models = ["SSD-1B", "stabilityai", "aesthetic", "stable_diffusion_v1_5"]
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(
                    self.process_model,
                    models,
                    [prompt] * len(models),
                    [images_list] * len(models),
                    [self.prompt_model_huggface] * len(models),
                )
        except Exception as e:
            print(f"Error: {e}")

        return {"image_paths": images_list}

    def prompt_model_huggface(self, model, prompt, images_list):
        try:
            url = self.helper.get_url_model_api(model)
            headers = self.helper.get_header_api()
            image_name = self.helper.generate_random_filename_image()
            image_path = os.path.join(self.script_dir, image_name)
            payload = {
                "inputs": prompt,
            }
            response = requests.post(url, headers=headers, json=payload)
            image_bytes = response.content
            try:
                print("make_request")
                self.save_image(image_bytes, image_path)
                image_path = self.save_image_supabase(image_path, image_name)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Image Bytes: {image_bytes[:20]}")
                image_path = ""
            if image_path:
                images_list.append(image_path)
        except Exception as e:
            print(f"Error processing model: {e}")

    ## Huggface endpoint
    def gen_image_huggface_endpoint(self):
        prompt = self.req["text_tran_user"]
        images_list = []
        models = ["SSD1", "SSD1", "SSD1", "SSD1"]
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(
                    self.process_model,
                    models,
                    [prompt] * len(models),
                    [images_list] * len(models),
                    [self.prompt_model_huggface_endpoint] * len(models),
                )
        except Exception as e:
            print(f"Error: {e}")

        return {"image_paths": images_list}

    def prompt_model_huggface_endpoint(self, model, prompt, images_list):
        image_name = self.helper.generate_random_filename_image()
        image_path = os.path.join(self.script_dir, image_name)
        image_bytes = SSD1(prompt).gen_image()
        try:
            print("make_my_request")
            self.save_image(image_bytes, image_path)
            image = self.save_image_supabase(image_path, image_name)
            if image:
                images_list.append(image)
            else:
                raise
        except Exception as e:
            print(f"Error: {e}")
            print(f"Image Bytes: {image_bytes[:20]}")

    # Bing
    def gen_image_bing(self):
        try:
            prompt = self.req["text_tran_user"]
            images_list = []
            image_text_generator = ImageTextGenerator4(prompt)
            results = image_text_generator.generate_images_text()
            print("results[0]", results[0])
            for r in results[0]:
                images_list.append(r)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Use executor.map with two iterable arguments
                # The first iterable should be the list of images
                # The second iterable should be the function to process each image
                results = list(executor.map(self.process_image, images_list))
                print("results", results)
                # Do something with the results if needed
        except Exception as e:
            print(f"Error with Bing, trying Huggface Endpoint: {e}")

    def process_image(self, url):
        try:
            image_bytes = self.get_image_from_url(url)
            if image_bytes and image_bytes is not None:
                image_name = self.helper.generate_random_filename_image()
                image_path = os.path.join(self.script_dir, image_name)
                self.save_image(image_bytes, image_path)
                image_path = self.save_image_supabase(image_path, image_name)
                return image_path
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def get_image_from_url(self, url, max_attempts=10, retry_interval=3):
        for attempt in range(1, max_attempts + 1):
            try:
                headers = {
                    "authority": "tse2.mm.bing.net",
                    "method": "GET",
                    "path": urlparse(url).path,
                    "scheme": "https",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                    "Cache-Control": "max-age=0",
                    "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                    "Sec-Ch-Ua-Arch": '""',
                    "Sec-Ch-Ua-Bitness": '"64"',
                    "Sec-Ch-Ua-Full-Version": '"118.0.5993.117"',
                    "Sec-Ch-Ua-Full-Version-List": '"Chromium";v="118.0.5993.117", "Google Chrome";v="118.0.5993.117", "Not=A?Brand";v="99.0.0.0"',
                    "Sec-Ch-Ua-Mobile": "?1",
                    "Sec-Ch-Ua-Model": '"Nexus 5"',
                    "Sec-Ch-Ua-Platform": '"Android"',
                    "Sec-Ch-Ua-Platform-Version": '"6.0"',
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
                }

                response = requests.get(url, headers=headers)
                # print(response.content)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                print(f"Error getting image from URL (attempt {attempt}): {e}")
                time.sleep(retry_interval)  # Add a delay before the next attempt
        print(f"Failed after {max_attempts} attempts.")
        return ""

    def save_image_supabase(self, filepath, image_name):
        try:
            if filepath is None:
                print("Error: Filepath is None")
                return None

            with open(filepath, "rb") as f:
                response = supabase.storage.from_("ChatImage").upload(
                    file=f, path=image_name
                )
            print(response.json())
            response = response.json()
            public_url = response["Key"]
            print(f"Image uploaded to Supabase: {public_url}")
            return public_url
        except Exception as e:
            print(f"Error saving image to Supabase: {e}")
            return None

    def save_image(self, image_bytes, image_path):
        image = Image.open(io.BytesIO(image_bytes))
        watermark_path = os.path.abspath("logo.png")
        watermark = Image.open(watermark_path)
        watermark = watermark.resize((50, 50))
        image.paste(watermark, (10, image.height - watermark.height - 10))
        image.save(image_path)
