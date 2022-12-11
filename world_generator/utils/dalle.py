"""The Edge of Reality
"""
from io import BytesIO
from uuid import uuid4
import requests
from typing import Optional

import openai
from PIL import Image

from config import FRAME_SIZE
from world_generator.utils.types import WorldFrame
from world_generator.utils.masks import sides_mask, right_mask, circled_mask


def generate_next_frame_url(src_img: str, **kw_settings) -> str:
    """Given a `src_image`, returns the next `FRAME_SIZE` pixels to the right
    """
    # Get right half of original:
    original = Image.open(src_img)
    left_half = original.crop((FRAME_SIZE // 2, 0, FRAME_SIZE, FRAME_SIZE))

    # Create a new image that will be the right half and empty
    without_right = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE))
    without_right.paste(left_half, (0, 0))

    # Convert image to bytes
    im_bytes = BytesIO()
    without_right.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=right_mask(size=4),
        **kw_settings
    )
    image_url = response['data'][0]['url']
    return image_url


def generate_last_frame_url(first_img: str, last_img: str, **kw_settings) -> str:
    """Given a `src_image`, returns the next 256 pixel to the right
    """
    # Get right half of original:
    first = Image.open(first_img)
    last = Image.open(last_img)

    # cropped_img = img.crop((left, top, right, bottom))

    left_half = last.crop((FRAME_SIZE // 4 * 3, 0, FRAME_SIZE, FRAME_SIZE))
    right_half = first.crop((0, 0, FRAME_SIZE // 3 * 2, FRAME_SIZE))

    # Create a new image that will be the right half and empty
    new = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE))
    new.paste(left_half, (0, 0))
    new.paste(right_half, (FRAME_SIZE // 4 * 3, 0))
    # new.save('.tmpfiles/debug_before_last.png')
    
    # Convert image to bytes
    im_bytes = BytesIO()
    new.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=sides_mask(),
        **kw_settings
    )
    image_url = response['data'][0]['url']
    return image_url


def download_image(url: str, dst: Optional[str] = None) -> WorldFrame:
    """
    """
    dst = dst if dst else f'.tmpfiles/{uuid4()}.png'
    print(f'Downloading from url: {url} to {dst}')
    image_data = requests.get(url)
    image = Image.open(BytesIO(image_data.content))
    image.save(dst)
    return WorldFrame(path=dst, image=image)


def generate_frame_variation(frame: WorldFrame, **kw_settings) -> WorldFrame:
    """Given a `src_image`, returns the next 256 pixel to the right
    """
    # Save the image to a BytesIO object
    im_bytes = BytesIO()
    frame['image'].save(im_bytes, format='PNG')
    
    kw_settings["prompt"] = kw_settings["prompt"] + 'psychedelic' 
    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=circled_mask(),
        **kw_settings
    )
    image_url = response['data'][0]['url']
    return image_url
