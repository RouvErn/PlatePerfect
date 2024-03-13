import requests

# Define the endpoint URL
url = "http://localhost:8000/predict"

# Prepare the image files
files = [
    ("image_files", ("image1.jpg", open("/Users/RouvenErnst/Downloads/IMG_4693.jpeg", "rb"), "image/jpeg")),
]
# Specify the serving size
payload = {"serving_size_grams": 450}

# Make the request
response = requests.post(url, files=files, data=payload)

# Print the response
print(response.json())
