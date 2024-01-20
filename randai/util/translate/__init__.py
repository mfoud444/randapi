from .google import  translate_google_deep

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
