from microsofttranslator import Translator

def translate_microsoft(prompt: str, dest: str = 'en'):
    translator = Translator(prompt, dest=dest)
    return translations.text
