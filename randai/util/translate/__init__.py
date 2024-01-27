from .google import  translate_google_deep
import re
class TextTran:
    def translate(self, prompt: str, dest: str = 'en', max_attempts: int = 3):
        translation_result = None

        for attempt in range(1, max_attempts + 1):
            try:
                # Try translating the text using different translation methods
                # You can uncomment the desired translation method here
                translation_result = translate_google_deep(prompt, dest=dest)
                # translation_result = translate_google_new(prompt, dest=dest)
                # translation_result = translate_google(prompt, dest=dest)

                if translation_result is not None:
                    print(f"Translation successful (attempt {attempt}): {translation_result}")
                    break  # Break out of the loop if translation is successful
                else:
                    print(f"Translated text is empty (attempt {attempt})")
            except Exception as e:
                print(f"Translation attempt {attempt} failed: {e}")

                if attempt < max_attempts:
                    print("Retrying translation...")
                else:
                    print("Max attempts reached, translation failed.")

        return translation_result

    def remove_code_blocks(self, markdown_text):
        code_block_pattern = re.compile(r'```.*?```', re.DOTALL)
        return code_block_pattern.sub('__CODE_BLOCK_PLACEHOLDER__', markdown_text)

    def translate_without_code(self, markdown_text, lang_code):
        text_without_code = self.remove_code_blocks(markdown_text)
        res_translate = self.translate(text_without_code, lang_code)
        translated_text_with_code = markdown_text
        if res_translate:
            translated_text_with_code = self.insert_code_blocks(res_translate, markdown_text)
        return translated_text_with_code
    
    def insert_code_blocks(self, translated_text, original_text):
        code_blocks = re.findall(r'```.*?```', original_text, re.DOTALL)
        for code_block in code_blocks:
            translated_text = translated_text.replace('__CODE_BLOCK_PLACEHOLDER__', code_block, 1)
        return translated_text.replace('__CODE_BLOCK_PLACEHOLDER__', '')