from PIL import Image

width, height = 1024, 1024


black = Image.new('RGBA', (width // 3, height), (0, 0, 0, 255))


# Create a new image that will be the right half and empty
new = Image.new('RGBA', (width, height))

new.paste(black, (0, 0))
new.paste(black, (width // 3 * 2, 0))

new.save('middle_mask.png')