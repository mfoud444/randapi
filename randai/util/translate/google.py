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
    max_char = 4900
    if 0 <= len(prompt) <= max_char:
        translate_text = GoogleTranslator(source='auto', target=dest).translate(prompt)
        return translate_text
    elif len(prompt) > max_char:
        chunks = [prompt[i:i+max_char] for i in range(0, len(prompt), max_char)]
        translated_chunks = [GoogleTranslator(source='auto', target=dest).translate(chunk) for chunk in chunks]
        return ''.join(translated_chunks)
    else:
        return f"Input prompt length should be between 0 and {max_char} characters."
