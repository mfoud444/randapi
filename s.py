from g4f.client import Client

client = Client()
response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",

)
image_url = response.data[0].url


# import g4f

# # Setting up the request for image creation
# response = g4f.ChatCompletion.create(
#     model=g4f.models.default, # Using the default model
#     provider=g4f.Provider.Ta, # Specifying the provider as Gemini
#     messages=[{"role": "user", "content": "Create an image like this"}],
#     image=open("/home/mohammed/Projects/backendrand/randapi/randai/logo.png", "rb"), # Image input can be a data URI, bytes, PIL Image, or IO object
#     image_name="logo.png" # Optional: specifying the filename
# )

# # Displaying the response
# print(response)