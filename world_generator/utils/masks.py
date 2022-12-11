"""Masks module create DALL-E Mask Image like explained here: https://beta.openai.com/docs/guides/images/edits
"""
from io import BytesIO
from random import randint

from PIL import Image, ImageDraw

from config import F_SIZE


def sides_mask() -> bytes:
    """Generate a mask with left and right borders
    """
    mask = Image.new('RGBA', (F_SIZE, F_SIZE))
    black_part = Image.new('RGBA', (F_SIZE // 4, F_SIZE), (0, 0, 0, 255))
    mask.paste(black_part, (0, 0))
    mask.paste(black_part, (F_SIZE // 4 * 3, 0))
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def right_mask(size: int = 2) -> bytes:
    """
    """
    mask = Image.new('RGBA', (F_SIZE, F_SIZE))
    black = Image.new('RGBA', (F_SIZE // size, F_SIZE), (0, 0, 0, 255))
    mask.paste(black, (0, 0))
    # mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def circled_mask() ->  bytes:
    mask = Image.new('RGBA', (F_SIZE, F_SIZE), (0, 0, 0, 255))

    r = F_SIZE // 2
    minimum_x = F_SIZE // 4
    maximum_x = F_SIZE - F_SIZE // 4 - r
    maximum_y = F_SIZE - r

    rand_x = randint(minimum_x, maximum_x)
    rand_y = randint(0, maximum_y)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((rand_x, rand_y, rand_x + r, rand_y + r), fill=(255, 255, 255, 0))
    mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()
