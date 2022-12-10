"""The Edge of Reality
"""
from uuid import uuid4
from time import perf_counter
from io import BytesIO
import requests
from PIL import Image

import openai
import time


start_time = perf_counter()

openai.api_key = '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'
prompt = "Equirectangular render of an alien world, 8k uhd"
base_size = 512
iterations = 1
settings = {"n": 1, "size": f"{base_size}x{base_size}", "prompt": prompt}

downloaded_index = 0

def get_next(src_img: str) -> str:
    """Given a `src_image`, returns the next `base_size` pixels to the right
    """
    # Get right half of original:
    original = Image.open(src_img)
    left_half = original.crop((base_size // 2, 0, base_size, base_size))

    # Create a new image that will be the right half and empty
    without_right = Image.new('RGBA', (base_size, base_size))
    without_right.paste(left_half, (0, 0))

    # Convert image to bytes
    im_bytes = BytesIO()
    without_right.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=open("masks/right_small.png", "rb"),
        **settings
    )
    image_url = response['data'][0]['url']
    return image_url


def get_last(first_img: str, last_img: str) -> str:
    """Given a `src_image`, returns the next 256 pixel to the right
    """
    # Get right half of original:
    first = Image.open(first_img)
    last = Image.open(last_img)

    # cropped_img = img.crop((left, top, right, bottom))

    left_half = last.crop((base_size // 3 * 2, 0, base_size, base_size))
    right_half = first.crop((0, 0, base_size // 3 * 2, base_size))


    # Create a new image that will be the right half and empty
    new = Image.new('RGBA', (base_size, base_size))
    new.paste(left_half, (0, 0))
    new.paste(right_half, (base_size // 3 * 2, 0))
    new.save('.tmpfiles/tempmother.png')
    # Convert image to bytes
    im_bytes = BytesIO()
    new.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=open("masks/middle_small.png", "rb"),
        **settings
    )
    image_url = response['data'][0]['url']
    return image_url


def download_image(url: str):
    """
    """
    print(f'Downloading from url: {url}')
    global downloaded_index
    image_data = requests.get(url)
    _image_name = f'.tmpfiles/{downloaded_index}.png'
    downloaded_index += 1
    image = Image.open(BytesIO(image_data.content))
    image.save(_image_name)
    return image, _image_name

print('******************************')
print('Genereting the first image...')
response = openai.Image.create(**settings)
image_url = response['data'][0]['url']
pillow_image, image_location = download_image(image_url)
images = [pillow_image]

first = image_location
last = image_location
for i in range(iterations):
    print(f'Genereting the image {i + 2} image...')
    next_url = get_next(image_location)
    pillow_image, image_location = download_image(next_url)
    last = image_location
    images.append(pillow_image)



print(f'Genereting the LAST image...')
last_url = get_last(first, last)
last_pillow_image, last_image_location = download_image(last_url)
last_pillow_image.save('.tmpfiles/finilized.png')

print('******************************')
print("Merging all images together...")
# Create a new image that will contain all of the merged images
init_width = sum([i.size[0] for i in images])
total_width = (init_width / 2) + (base_size / 2) + (base_size / 3)
new_image = Image.new('RGB', (int(total_width), base_size))

# Paste each image into the new image
x_offset = 0
for i, image in enumerate(images):
    new_image.paste(image, (x_offset, 0))
    print(f"Pasted image {i}")
    x_offset += image.size[0] - (base_size // 2)

x_offset = x_offset + (base_size // 2) - (base_size // 3)
new_image.paste(last_pillow_image, (x_offset, 0))

# Save the merged image
new_image.save(f'examples/full_{uuid4()}.png')

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"It took {elapsed_time:.2f} seconds to run.")