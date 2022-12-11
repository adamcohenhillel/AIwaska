"""The Edge of Reality
"""
from io import BytesIO

from PIL import Image, ImageDraw


def sides_mask(frame_size: int = 512) -> bytes:
    """Generate a mask with left and right borders
    """
    mask = Image.new('RGBA', (frame_size, frame_size))
    black_part = Image.new('RGBA', (frame_size // 4, frame_size), (0, 0, 0, 255))
    mask.paste(black_part, (0, 0))
    mask.paste(black_part, (frame_size // 4 * 3, 0))

    mask.paste(black_part, (frame_size // 4, 0))

    mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def right_mask(frame_size: int = 512, size: int = 2) -> bytes:
    """
    """
    mask = Image.new('RGBA', (frame_size, frame_size))
    black = Image.new('RGBA', (frame_size // size, frame_size), (0, 0, 0, 255))
    mask.paste(black, (0, 0))
    # mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def circled_mask(frame_size: int = 512) ->  bytes:
    mask = Image.new('RGBA', (frame_size, frame_size), (0, 0, 0, 255))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((200, 200, 384, 384), fill=(255, 255, 255, 0))
    # mask.save('debug.png')
    mask_bytes = BytesIO()
    mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()
