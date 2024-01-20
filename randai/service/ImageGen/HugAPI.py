import requests
import json
import time
import uuid
import os
from concurrent.futures import ThreadPoolExecutor

class HugAPI:
    def __init__(self, url, headers, data, folder_image='image'):
        self.url = url
        self.headers = headers
        self.data = data
        self.folder_image = folder_image
        self.max_retries = 5
        self.retry_delay = 60

    def gen_image(self) -> bytes:
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))

        if response.status_code == 200:
            image_data = response.content
            return image_data
        elif response.status_code == 503:
            try:
                estimated_time_milliseconds = float(response.json().get("estimated_time", 60000)) 
                print("estimated_time_milliseconds", estimated_time_milliseconds)
                estimated_time_seconds = estimated_time_milliseconds / 1000
                self.retry_delay = max(estimated_time_seconds, 5)
                print(f"Model is still loading. Retrying in {self.retry_delay} seconds. Status code: {response.status_code}")
                time.sleep(self.retry_delay)
                return self.gen_image()
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                time.sleep(self.retry_delay)
                return self.gen_image()
        else:
            print(f"Error: Failed to retrieve image. Status code: {response.status_code},{response.text}")
            return b''  # Return an empty bytes object to indicate failure
