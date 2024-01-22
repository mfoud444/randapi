from .g4ff3 import *
import time
from .g4ff3.Provider.bing import CreateImagesBing
from fp.fp import FreeProxy

class ImageTextGenerator:
    def __init__(self, prompt, max_attempts=5):
        self.prompt = prompt
        self.max_attempts = max_attempts
        self.results = []

    def generate_images_text(self):
        attempts = 0

        while attempts < self.max_attempts:
            try:
                bing_images_provider = CreateImagesBing()
                result_generator = bing_images_provider.create_completion(prompt=self.prompt)

                # Collect results in a list
                self.results.extend(result_generator)

                # Successful execution, break the loop
                break

            except (RuntimeError, Exception) as e:
                print(f"Error: {e}")
                print(f"Error during image creation (Attempt {attempts + 1}/{self.max_attempts})")
                attempts += 1

                # For the first attempt, add a delay
                if attempts == 1:
                    time.sleep(1)  # Add a delay between attempts if needed

        return self.results




# import time
# import concurrent.futures
# from .g4ff.Provider.bing import CreateImagesBing
# from fp.fp import FreeProxy
# class ImageTextGenerator:
#     def __init__(self, prompt, max_attempts=5):
#         self.prompt = prompt
#         self.max_attempts = max_attempts
#         self.results = []
        

#     def generate_images_text(self):
#         attempts = 0
#         # proxy = FreeProxy().get()
#         # print("proxy",proxy)

#         while attempts < self.max_attempts:
#             try:
#                 bing_images_provider = CreateImagesBing()
#                 result_generator = bing_images_provider.create_completion(prompt=self.prompt)

#                 # Collect results in a list
#                 self.results.extend(result_generator)

#                 # Successful execution, break the loop
#                 break

#             except (RuntimeError, Exception) as e:
#                 print(f"Error {e}")
#                 print(f"Error during image creation (Attempt {attempts + 1}/{self.max_attempts})")
#                 attempts += 1

#                 # For the first attempt, no need for threads
#                 if attempts == 1:
#                     time.sleep(1)  # Add a delay between attempts if needed
#                 else:
#                     # Use threads for subsequent attempts
#                     with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_attempts - 1) as executor:
#                         futures = [executor.submit(self._retry_attempt) for _ in range(self.max_attempts - 1)]
                        
#                         # Wait for the first successful result
#                         for future in concurrent.futures.as_completed(futures):
#                             if future.result() is not None:
#                                 break

#         return self.results

#     def _retry_attempt(self):
#         try:
#             bing_images_provider = CreateImagesBing()
#             result_generator = bing_images_provider.create_completion(self.prompt)

#             # Collect results in a list
#             self.results.extend(result_generator)
#             return True

#         except (RuntimeError, Exception) as e:
#             print(f"Error {e}")
#             return False