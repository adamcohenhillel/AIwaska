"""The Edge of Reality
"""
import itertools
from io import BytesIO
from uuid import uuid4
import requests
from typing import List, Dict, Optional

import openai
from PIL import Image

from worldgen.utils.decorators import print_execution_time
from worldgen.utils.types import WorldFrame
from worldgen.utils.masks import sides_mask, right_mask


# TODO: Better config
openai.api_key = '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'
_F_SIZE = 1024
_F_NUM = 3
#########


def generate_next_frame_url(src_img: str, **kw_settings) -> str:
    """Given a `src_image`, returns the next `_F_SIZE` pixels to the right
    """
    # Get right half of original:
    original = Image.open(src_img)
    left_half = original.crop((_F_SIZE // 2, 0, _F_SIZE, _F_SIZE))

    # Create a new image that will be the right half and empty
    without_right = Image.new('RGBA', (_F_SIZE, _F_SIZE))
    without_right.paste(left_half, (0, 0))

    # Convert image to bytes
    im_bytes = BytesIO()
    without_right.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=right_mask(frame_size=_F_SIZE, size=4),
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

    left_half = last.crop((_F_SIZE // 4 * 3, 0, _F_SIZE, _F_SIZE))
    right_half = first.crop((0, 0, _F_SIZE // 3 * 2, _F_SIZE))

    # Create a new image that will be the right half and empty
    new = Image.new('RGBA', (_F_SIZE, _F_SIZE))
    new.paste(left_half, (0, 0))
    new.paste(right_half, (_F_SIZE // 4 * 3, 0))
    # new.save('.tmpfiles/debug_before_last.png')
    
    # Convert image to bytes
    im_bytes = BytesIO()
    new.save(im_bytes, format='PNG')

    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=sides_mask(frame_size=_F_SIZE),
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
    
    kw_settings["prompt"] = 'psychedelic'
    # Get extend to the right right: 
    response = openai.Image.create_edit(
        image=im_bytes.getvalue(),
        mask=sides_mask(frame_size=_F_SIZE, variation=True),
        **kw_settings
    )
    image_url = response['data'][0]['url']
    return image_url


def merge_frames(frames: List[WorldFrame], dst: Optional[str] = None) -> None:
    """Merging all frames together, the last frame is used differently #TODO: Explain better
    """
    dst = dst if dst else f'examples/full_{uuid4()}.png'
    print('******************************')
    print('Merging all images together...')
    last_frame = frames.pop()

    # Create a new image that will contain all of the merged images
    init_width = sum([i['image'].size[0] for i in frames])
    total_width = (init_width / 2) + _F_SIZE
    new_image = Image.new('RGB', (int(total_width), _F_SIZE))

    # Paste each image into the new image
    x_offset = 0
    for i, frame in enumerate(frames):
        new_image.paste(frame['image'], (x_offset, 0))
        print(f'Pasted image {i}')
        x_offset += frame['image'].size[0] - (_F_SIZE // 2)

    x_offset = x_offset + (_F_SIZE // 4)
    new_image.paste(last_frame['image'], (x_offset, 0))

    # Save the merged image
    new_image.save(dst)


@print_execution_time
def main_loop(settings: Dict) -> None:
    """
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Create a JSON list of 20 related prompts that describe a \"{settings['prompt']}\".\nExample: [\"prompt1\", \"prompt2\", \"prompt3\"]\n\n[\"The sky is a rainbow of swirling colors\", \"Strange creatures darting through the clouds\", \"Gigantic crystals stretch up to the horizon\", \"The air is filled with a dream-like mist\", \"Floating islands filled with vibrant vegetation\", \"Trees of pink, purple, and blue\", \"Distant stars twinkle like neon lights\", \"Glimmering waterfalls cascading through the sky\", \"The ground is covered in a strange luminescent moss\", \"Gigantic mushrooms dot the landscape\", \"Gravity is unpredictable and ever-changing\", \"Time appears to stand still in this realm\", \"A soft, alien melody plays in the background\", \"The sun is a bright, multi-colored prism\", \"Creatures with tentacles and wings float by\", \"The moon is a giant swirling galaxy\", \"A river of stars leads to an unknown destination\", \"Strange creatures lurk in the shadows\", \"The horizon is a kaleidoscope of colors\", \"The trees whisper secrets in a strange language\"]",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    frames: List[WorldFrame] = []
    variation_frames: Dict[List[WorldFrame]] = {}
    last_path = ''
    for i in range(_F_NUM):
        print(f'\nGenereting frame #{i}...')
        if i == 0:
            response = openai.Image.create(**settings)
            url = response['data'][0]['url']
        elif i < _F_NUM - 1:
            url = generate_next_frame_url(last_path, **settings)
        else:
            url = generate_last_frame_url(frames[0]['path'], frames[-1]['path'], **settings)

        frame = download_image(url, dst=f'.tmpfiles/{i}.png')
        last_path = frame['path']
        frames.append(frame)
        
        if i not in variation_frames.keys():
            variation_frames[i] = []
    
        # VARIATIONS:
        if i > 0 and i < _F_NUM - 1:
            for j in range(1):
                v_url = generate_frame_variation(frame=frame, **settings)
                v_frame = download_image(v_url, dst=f'.tmpfiles/unique_{i}_{j}.png')
                variation_frames[i].append(v_frame)
        else:
            variation_frames[i].append(frame)


    merge_frames(frames)

    # VARIATIONS:
    tt = [b for b in variation_frames.values()]
    tt_2 = list(itertools.product(*tt))
    for i, c in enumerate(tt_2):
        merge_frames(list(c), dst=f"examples/variation_{i}.png")
