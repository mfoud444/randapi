import random
import string
from .Settings import Settings

class Helper:
    def __init__(self):
        self.settings = Settings()

    def generate_random_filename_image(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + '.png'

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.settings.ALLOWED_EXTENSIONS

    def make_url_image(self, image_path: str):
        return f"{self.settings.HOST}/api/get_image?path={image_path}"

    def get_url_model_api(self, model: str, default_model_image=None):
        if model in self.settings.MODEL_API_IMAGE_HUGG:
            return f"https://api-inference.huggingface.co/models/{self.settings.MODEL_API_IMAGE_HUGG[model]}"
        else:
            if default_model_image is not None:
                return f"https://api-inference.huggingface.co/models/{self.settings.MODEL_API_IMAGE_HUGG[self.settings.default_model_image]}"
            else:
                # Handle the case where the default model is not specified
                raise ValueError("Default model not specified in MODEL_API_IMAGE_HUGG")

    def get_header_api(self):
        return {"Authorization": f"Bearer {self.settings.TOKAN}"}
