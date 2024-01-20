
# import g4f
# response = g4f.ChatCompletion.create(
# model="gpt-4",
# provider=g4f.Provider.CreateImagesProvider,
# messages=[{"role": "user", "content": "what is this"}],
# stream = True,
# )
# for message in response:
#     print(message, flush=True, end='')
# import g4f
# response = g4f.ChatCompletion.create(
#     model="gpt-4",
#     provider=g4f.Provider.Bing,
#     messages=[{"role": "user", "content": "create image dog swimming "}],
# stream= False

# )
# for message in response:
#     print(message, flush=True, end='')
import g4f
print("sss")
bing_images_provider = g4f.Provider.bing.CreateImagesBing()
prompt = "cow yelow and red"
result_generator =  bing_images_provider.create_completion(prompt)

# Iterate over the generator to get the result
for result in result_generator:
    print(result)

