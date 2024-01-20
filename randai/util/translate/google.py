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
        translate_text = GoogleTranslator(source='auto', target=dest).translate(prompt)
        return translate_text
        print(translate_text)