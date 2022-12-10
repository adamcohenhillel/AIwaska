"""The Edge of Reality
"""
from io import BytesIO
import requests
from PIL import Image

import openai


openai.api_key = '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'
prompt = "High resolution, equirectangular render of a large open space with a theme of a city in the Middle Ages"

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
        mask=open("masks/right.png", "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


def get_last(first_img: str, last_img: str) -> str:
    """Given a `src_image`, returns the next 512 pixel to the right
    """
    # Get right half of original:
    first = Image.open(first_img)
    last = Image.open(last_img)
    width, height = first.size

    # cropped_img = img.crop((left, top, right, bottom))

    left_half = last.crop((width // 3 * 2, 0, width, height))
    right_half = first.crop((0, 0, width // 3 * 2, height))


    # Create a new image that will be the right half and empty
    new = Image.new('RGBA', (width, height))
    new.paste(left_half, (0, 0))
    new.paste(right_half, (width // 3 * 2, 0))
    new.save('tempmother.png')
    # Convert image to bytes
    im_bytes = BytesIO()
    new.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=open("masks/middle.png", "rb"),
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

first = image_location
last = image_location
for _ in range(4):
    next_url = get_next(image_location)
    pillow_image, image_location = download_image(next_url)
    last = image_location
    images.append(pillow_image)


last_url = get_last(first, last)
last_pillow_image, last_image_location = download_image(last_url)



#### Connect them all together:

# Create a new image that will contain all of the merged images
widths, heights = zip(*(i.size for i in images))
total_width = int(sum(widths) / 2) + (1024 // 3)
max_height = max(heights)
new_image = Image.new('RGB', (total_width, max_height))

# Paste each image into the new image
x_offset = 0
for im in images:
    new_image.paste(im, (x_offset, 0))
    x_offset += im.size[0] - 512

x_offset = x_offset + 512 - (1024 // 3)
new_image.paste(last_pillow_image, (x_offset, 0))

# Save the merged image
new_image.save('merged_image.png')