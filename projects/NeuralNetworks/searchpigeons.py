from decouple import config
from google_images_search import GoogleImagesSearch
import requests
import os
import shutil

output_dir = "pigeons_sexy_photos"
control = False

if control:
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)


api_key = config("key")
custom_search_engine_id = config("custom_id")

# initialize google images searc
GIS = GoogleImagesSearch(api_key, custom_search_engine_id)

# perform a google search
query = "pigeons on builds"
GIS.search({"q": query, "num": 10, "fileType": "jpg", "imgSize": "large"})

# download images:
for i, images in enumerate(GIS.results()):
    response = requests.get(images.url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(output_dir, f"{query}_{i}.jpg"), "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

print("Images piccioni scaricate béne")

