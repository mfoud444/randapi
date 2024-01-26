# from googletrans import Translator
# from google_trans_new import google_translator
from deep_translator import GoogleTranslator
# def translate_google(prompt: str, dest: str = 'en'):
#         translations = Translator().translate(prompt, dest=dest)
#         return translations.text

# def translate_google_new(prompt: str, dest: str = 'en'):
#         translator = google_translator()
#         translate_text = translator.translate(prompt, lang_tgt=dest)
#         return translate_text
#         print(translate_text)

def translate_google_deep(prompt: str, dest: str = 'en'):
    # Check if the input prompt is within the allowed length
    if 0 <= len(prompt) <= 5000:
        translate_text = GoogleTranslator(source='auto', target=dest).translate(prompt)
        return translate_text
    elif len(prompt) > 5000:
        # If the input prompt is too long, split it into chunks and translate each chunk
        chunks = [prompt[i:i+5000] for i in range(0, len(prompt), 5000)]
        translated_chunks = [GoogleTranslator(source='auto', target=dest).translate(chunk) for chunk in chunks]
        return ''.join(translated_chunks)
    else:
        # Handle the case where the input prompt is empty or negative length
        return "Input prompt length should be between 0 and 5000 characters."
