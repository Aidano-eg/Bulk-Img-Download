# install packages with:
# pip install pandas requests beautifulsoup4


import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Load the CSV file
file_path = "sports-logos.csv"  # Replace with your CSV file name
links_df = pd.read_csv(file_path)

# Create a folder to save images
os.makedirs("downloaded_images", exist_ok=True)

# List of common image file extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

for idx, row in links_df.iterrows():
    url = row['Link']  # Replace 'Link' with the actual column name for URLs in your CSV
    image_name = row['Name']  # Replace 'Name' with the actual column name for image names in your CSV

    try:
        if url.lower().endswith(image_extensions):
            # Download the image directly
            img_data = requests.get(url).content
            img_name = f"downloaded_images/{image_name}.png"  # Save with the name from the "Name" column
            with open(img_name, "wb") as handler:
                handler.write(img_data)
            print(f"Downloaded image from direct link {url} as {img_name}")
        else:
            # Fetch the page and try to find an <img> tag
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the first image on the page
            img_tag = soup.find("img")
            if img_tag and img_tag.get("src"):
                img_url = img_tag.get("src")
                
                # Make the URL absolute if it's relative
                if not img_url.startswith("http"):
                    img_url = requests.compat.urljoin(url, img_url)
                
                # Download the image
                img_data = requests.get(img_url).content
                img_name = f"downloaded_images/{image_name}.jpg"  # Save with the name from the "Name" column
                with open(img_name, "wb") as handler:
                    handler.write(img_data)
                print(f"Downloaded image from {url} as {img_name}")
            else:
                print(f"No image found at {url}")
    except Exception as e:
        print(f"Failed to process {url}: {e}")
