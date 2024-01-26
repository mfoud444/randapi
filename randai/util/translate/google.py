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
    max_chunk_size = 5000

#     if not (0 <= len(prompt) <= max_chunk_size):
#         raise ValueError("Input prompt length should be between 0 and 5000 characters.")

    translator = google_translator.GoogleTranslator()

    # Check if the prompt exceeds the maximum chunk size
    if len(prompt) > max_chunk_size:
        # Split the prompt into chunks
        chunks = [prompt[i:i+max_chunk_size] for i in range(0, len(prompt), max_chunk_size)]
        
        # Translate each chunk and concatenate the results
        translated_text = ''.join(translator.translate(chunk, lang_tgt=dest) for chunk in chunks)
    else:
        # If the prompt is within the limit, translate it directly
        translated_text = translator.translate(prompt, lang_tgt=dest)

    return translated_text
