"""Masks module create DALL-E Mask Image like explained here: https://beta.openai.com/docs/guides/images/edits
"""
from io import BytesIO
from random import randint

from PIL import Image, ImageDraw

from config import FRAME_SIZE


def sides_mask() -> bytes:
    """Generate a mask with left and right borders
    """
    mask = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE))
    black_part = Image.new('RGBA', (FRAME_SIZE // 4, FRAME_SIZE), (0, 0, 0, 255))
    mask.paste(black_part, (0, 0))
    mask.paste(black_part, (FRAME_SIZE // 4 * 3, 0))
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def right_mask(size: int = 2) -> bytes:
    """
    """
    mask = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE))
    black = Image.new('RGBA', (FRAME_SIZE // size, FRAME_SIZE), (0, 0, 0, 255))
    mask.paste(black, (0, 0))
    # mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def circled_mask() ->  bytes:
    mask = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE), (0, 0, 0, 255))

    r = FRAME_SIZE // 3
    minimum_x = FRAME_SIZE // 4
    maximum_x = (FRAME_SIZE // 4 * 3) - (r//2)
    maximum_y = FRAME_SIZE - (r//2)

    rand_x = randint(minimum_x, maximum_x)
    rand_y = randint(0, maximum_y)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((rand_x, rand_y, rand_x + r, rand_y + r), fill=(255, 255, 255, 0))
    mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()
