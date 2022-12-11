"""The Edge of Reality
"""
from io import BytesIO

from PIL import Image, ImageDraw


# Non-Middle Mask:
def sides_mask(frame_size: int = 512) -> bytes:
    """Generate a mask with left and right borders
    """
    middle_mask = Image.new('RGBA', (frame_size, frame_size))
    black_part = Image.new('RGBA', (frame_size // 4, frame_size), (0, 0, 0, 255))
    middle_mask.paste(black_part, (0, 0))
    middle_mask.paste(black_part, (frame_size // 4 * 3, 0))
    # middle_mask.save('debug.png')
    mask_bytes = BytesIO()
    middle_mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def right_mask(frame_size: int = 512) -> bytes:
    """
    """
    right_mask = Image.new('RGBA', (frame_size, frame_size))
    black = Image.new('RGBA', (frame_size // 2, frame_size), (0, 0, 0, 255))
    right_mask.paste(black, (0, 0))
    # right_mask.save('debug.png')
    mask_bytes = BytesIO()
    right_mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()


def circled_mask(frame_size: int = 512) ->  bytes:
    circle_mask = Image.new('RGBA', (frame_size, frame_size), (0, 0, 0, 255))
    draw = ImageDraw.Draw(circle_mask)
    draw.ellipse((10, 10, 502, 502), fill=(255, 255, 255, 0))
    # circle_mask.save('debug.png')
    mask_bytes = BytesIO()
    circle_mask.save(mask_bytes, format='PNG')
    return mask_bytes.getvalue()
