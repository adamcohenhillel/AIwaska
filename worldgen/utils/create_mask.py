from PIL import Image

width, height = 512, 512

middle_mask = Image.new('RGBA', (width, height))
black_part = Image.new('RGBA', (width // 3, height), (0, 0, 0, 255))
middle_mask.paste(black_part, (0, 0))
middle_mask.paste(black_part, (width // 3 * 2, 0))
middle_mask.save('right_mask.png')


right_mask = Image.new('RGBA', (width, height))
black = Image.new('RGBA', (width // 2, height), (0, 0, 0, 255))
right_mask.paste(black, (0, 0))
right_mask.save('right_mask.png')