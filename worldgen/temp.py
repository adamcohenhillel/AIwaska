"""The Edge of Reality
"""
from uuid import uuid4
from io import BytesIO
import requests
from PIL import Image

import openai


openai.api_key = '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'
prompt = "Equirectangular render of an open space with a theme of a Hyde park, Lonodn, 4K"

index = 0

def get_next(src_img: str) -> str:
    """Given a `src_image`, returns the next 512 pixel to the right
    """
    # Get right half of original:
    original = Image.open(src_img)
    width, height = original.size
    left_half = original.crop((width // 2, 0, width, height))

    # Create a new image that will be the right half and empty
    without_right = Image.new('RGBA', (width, height))
    without_right.paste(left_half, (0, 0))

    # Convert image to bytes
    im_bytes = BytesIO()
    without_right.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=open("images/left_mask.png", "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

def download_image(url: str):
    """
    """
    global index
    image_data = requests.get(url)
    _image_name = f'{index}.png'
    index += 1
    image = Image.open(BytesIO(image_data.content))
    image.save(_image_name)
    return image, _image_name


response = openai.Image.create(prompt=prompt, n=1,size="1024x1024")
image_url = response['data'][0]['url']
pillow_image, image_location = download_image(image_url)
images = [pillow_image]

for _ in range(5):
    next_url = get_next(image_location)
    pillow_image, image_location = download_image(next_url)
    images.append(pillow_image)




#### Connect them all together:

# Create a new image that will contain all of the merged images
widths, heights = zip(*(i.size for i in images))
total_width = int(sum(widths) / 2)
max_height = max(heights)
new_image = Image.new('RGB', (total_width, max_height))

# Paste each image into the new image
x_offset = 0
for im in images:
    new_image.paste(im, (x_offset, 0))
    x_offset += im.size[0] - 512

# Save the merged image
new_image.save('merged_image.png')