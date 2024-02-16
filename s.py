import g4f

# Setting up the request for image creation
response = g4f.ChatCompletion.create(
    model=g4f.models.default, # Using the default model
    provider=g4f.Provider.Gemini, # Specifying the provider as Gemini
    messages=[{"role": "user", "content": "Create an image like this"}],
    image=open("/home/mohammed/Projects/randapi/randai/logo.png", "rb"), # Image input can be a data URI, bytes, PIL Image, or IO object
    image_name="logo.png" # Optional: specifying the filename
)

# Displaying the response
print(response)