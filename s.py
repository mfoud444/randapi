import requests
import base64

def image_path_to_data_uri(image_path):
    try:
        # Construct the full URL
        supabase_url_file = 'https://fvpmikdmeystnnxnloqe.supabase.co/storage/v1/object/public/chat-text/' + image_path
        print(supabase_url_file)

        # Make an HTTP request to get the image content
        response = requests.get(supabase_url_file)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Read the image content
            image_data = response.content

            # Encode the image data in base64
            base64_encoded_image = base64.b64encode(image_data).decode("utf-8")

            # Determine the image format based on the file extension
            file_extension = image_path.split(".")[-1]
            image_format = "jpeg" if file_extension.lower() == "jpg" else file_extension.lower()

            # Construct the data URI
            data_uri = f"data:image/{image_format};base64,{base64_encoded_image}"

            return data_uri
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error converting image to data URI: {e}")
        return None




import base64

def image_path_to_data_uri1(image_path):
    try:
        with open(image_path, "rb") as image_file:
            # Read the image file
            image_data = image_file.read()

            # Encode the image data in base64
            base64_encoded_image = base64.b64encode(image_data).decode("utf-8")

            # Determine the image format based on the file extension
            file_extension = image_path.split(".")[-1]
            image_format = "jpeg" if file_extension.lower() == "jpg" else file_extension.lower()

            # Construct the data URI
            data_uri = f"data:image/{image_format};base64,{base64_encoded_image}"

            return data_uri
    except Exception as e:
        print(f"Error converting image to data URI: {e}")
        return None
import g4f
import sys
from typing import Any, AsyncGenerator, Generator, NewType, Tuple, Union, List, Dict, Type, IO
from PIL.Image import Image
# Example usage
image_path = 'ChatText/Screenshot from 2024-01-03 23-43-22.png'
data_uri = True#image_path_to_data_uri(image_path)
ImageType = Union[str, bytes, IO, Image, None]
# image_path = '/home/mohammed/Projects/randdaj/randai/service/logo.png'
# data_uri = image_path_to_data_uri1(image_path)
if data_uri:
    # print(f"Data URI for {image_path}:\n{data_uri}")
    
    g4f.debug.logging = True 
    g4f.debug.version_check = True
    # print(g4f.Provider.bing.CreateImagesBing)
    # res = g4f.CreateImagesProvider.CreateImagesBing.create_completion
    # print(g4f.Provider.bing.create_images)

    response = g4f.ChatCompletion.create(
        model="gpt-4",
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": "create image dog"}],
   

    )
    for message in response:
        print(message, flush=True, end='')
    
# from g4f import ChatCompletion

# params = {
#                         "model": 'gpt-4',
#                         "messages": [{'role': 'system', 'content': 'Use emojis in your answers, Start your answer by "Hello, I am Rand AI, developed by Mohammed Foud"'}, {'role': 'user', 'content': 'Implement responsive designs'}],
#                         "stream":True,
                  
#                         "provider":"Llama2"
#                     }

# response = ChatCompletion.create(**params)

# for chunk in response:
#     print(chunk, flush=True, end='')
    
# print(response)
