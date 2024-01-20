

from g4f.Provider.bing import create_completion
print("sss")
# bing_images_provider = CreateImagesBing()
prompt = "cow yelow and red"
result_generator = create_completion(prompt)

# Iterate over the generator to get the result
for result in result_generator:
    print(result)