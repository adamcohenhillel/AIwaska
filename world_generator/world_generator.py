"""The Edge of Reality
"""
import itertools
from uuid import uuid4
from typing import List, Dict, Optional

import openai
from PIL import Image

from config import F_SIZE, F_NUM
from world_generator.utils.dalle import (
    download_image,
    generate_frame_variation,
    generate_last_frame_url,
    generate_next_frame_url
)
from world_generator.utils.decorators import print_execution_time
from world_generator.utils.gpt import get_prompt_variations
from world_generator.utils.types import WorldFrame


def merge_frames(frames: List[WorldFrame], dst: Optional[str] = None) -> None:
    """Merging all frames together, the last frame is used differently #TODO: Explain better
    """
    dst = dst if dst else f'examples/full_{uuid4()}.png'
    print('******************************')
    print('Merging all images together...')
    last_frame = frames.pop()

    # Create a new image that will contain all of the merged images
    init_width = sum([i['image'].size[0] for i in frames])
    total_width = (init_width / 2) + F_SIZE
    new_image = Image.new('RGB', (int(total_width), F_SIZE))

    # Paste each image into the new image
    x_offset = 0
    for i, frame in enumerate(frames):
        new_image.paste(frame['image'], (x_offset, 0))
        print(f'Pasted image {i}')
        x_offset += frame['image'].size[0] - (F_SIZE // 2)

    x_offset = x_offset + (F_SIZE // 4)
    new_image.paste(last_frame['image'], (x_offset, 0))

    # Save the merged image
    new_image.save(dst)


@print_execution_time
def generate_new_world(settings: Dict, dst: str) -> None:
    """
    """
    frames: List[WorldFrame] = []
    variation_frames: Dict[List[WorldFrame]] = {}
    last_path = ''
    prompt_variations = get_prompt_variations(settings['prompt'], num=5)

    for i in range(F_NUM):
        print(f'\nGenereting frame #{i}...')
        if i == 0:
            response = openai.Image.create(**settings)
            url = response['data'][0]['url']
        elif i < F_NUM - 1:
            url = generate_next_frame_url(last_path, **settings)
        else:
            url = generate_last_frame_url(frames[0]['path'], frames[-1]['path'], **settings)

        frame = download_image(url, dst=f'.tmpfiles/{i}.png')
        last_path = frame['path']
        frames.append(frame)
        
        if i not in variation_frames.keys():
            variation_frames[i] = []
    
        # VARIATIONS:
        if i > 0 and i < F_NUM - 1:
            for j, var in enumerate(prompt_variations):
                s = settings.copy()
                s['prompt'] = var
                v_url = generate_frame_variation(frame=frame, **settings)
                v_frame = download_image(v_url, dst=f'.tmpfiles/unique_{i}_{j}.png')
                variation_frames[i].append(v_frame)
        elif len(variation_frames[i]) == 0:
            variation_frames[i].append(frame)


    merge_frames(frames, dst=f'{dst}/_variation_og.png')
    # VARIATIONS:
    tt = [b for b in variation_frames.values()]
    tt_2 = list(itertools.product(*tt))
    for i, c in enumerate(tt_2):
        merge_frames(list(c), dst=f'{dst}/variation_{i}.png')
