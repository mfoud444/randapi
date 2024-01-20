import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
import uuid

url = "https://api-inference.huggingface.co/models/segmind/SSD-1B"

headers = {
    "content-type": "application/json",
    "sec-ch-ua": '"Chromium";v="119", "Opera";v="105", "OperaMobile";v="79", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 11; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.193 Mobile Safari/537.36 OPR/79.2.4195.76518",
    "x-use-cache": "false",
    "sec-ch-ua-platform": '"Android"',
    "accept": "*/*",
    "origin": "https://huggingface.co",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://huggingface.co/",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    # "cookie": "__stripe_mid=42e4e336-0597-4149-be33-6fd53084dbb559be91; _gcl_au=1.1.527810818.1699137072; ph_phc_Tbfg4EiRsr5iefFoth2Y1Hi3sttTeLQ5RV5TLg4hL1W_posthog=%7B%22distinct_id%22%3A%2218b9c763b6b5-0c4a9dfa408672-3c01777c-51a6b-18b9c763b6c74%22%2C%22%24device_id%22%3A%2218b9c763b6b5-0c4a9dfa408672-3c01777c-51a6b-18b9c763b6c74%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22%24sesid%22%3A%5B1699137105425%2C%2218b9c763d6ba5-07a345fbc3799f-3c01777c-51a6b-18b9c763d6ce1%22%2C1699137076586%5D%2C%22%24session_recording_enabled_server_side%22%3Afalse%2C%22%24autocapture_disabled_server_side%22%3Afalse%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%7D; _ga=GA1.1.874547381.1694037902; token=yjaUkoBvnmGpdhGnIrHWfrOjcNObZfMFIEgsQRZgFYIDXLrTsDIlOPqgYzraVDXajlkKbEvFfhPRfojFQoJiFdmttNyKGgJNOTRYNhkuEqWGizsagOGJoGERjQmwAywA; __stripe_sid=72328325-3213-4fba-8848-894172f7b64ec033e1; _ga_8Q63TH4CSL=GS1.1.1705671905.41.0.1705671905.60.0.0; aws-waf-token=7b732d36-96b1-4574-a804-5eab0f2aedc0:DwoAtrBgm58QAAAA:Nkxk/rpEvxYlYubwVLM2fud65XJHgG/6mMrAZMVBPYWR3QHV3gxm1wF+bZyYLKm8O4vK4RsJHv5fzQ+Sk5/DmgszxHmgUu35i3l6SMFnwVpy/vQBfmRCBPDqMxiMgt44gwzlI8LujKHXeU7QXdkUtz9C5IuzEGX3RPs26IZjFm4JaECr5A1meoJardvujoBnRN+6R8gn9Ne/YbuFr9WuK3WdfRv049Kwv/n6VvI4TWuc+j9tItj+6+C4913U51gTmQ1PsaiXm4/0jhrO2A=="
}

data = {
    "inputs": "red dog"
}
Folder_Image = 'image'

def download_image(attempt):
    for retry in range(1, max_retries + 1):
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            # Generate a random filename using UUID
            image_filename = f"{Folder_Image}/image_{attempt}_{uuid.uuid4().hex[:8]}.png"

            # Ensure the folder exists
            os.makedirs(Folder_Image, exist_ok=True)

            with open(image_filename, "wb") as image_file:
                image_file.write(response.content)

            print(f"Image {attempt} saved successfully as {image_filename}.")
            break
        elif response.status_code == 503:
            print(response.text)
            print(f"Model is still loading. Retry {retry}/{max_retries}. Waiting {retry_delay} seconds.")
            time.sleep(retry_delay)
        else:
            print(response.text)
            print(f"Error: Failed to retrieve image {attempt}. Status code: {response.status_code}")
            break

# Set the maximum number of retries
max_retries = 5

# Set the delay between retries in seconds
retry_delay = 60

# Number of images to download concurrently
num_images = 20

with ThreadPoolExecutor(max_workers=num_images) as executor:
    # Schedule download tasks concurrently
    executor.map(download_image, range(1, num_images + 1))
