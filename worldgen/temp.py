"""The Edge of Reality

"""
# import json
# from json.decoder import JSONDecodeError

# import openai


# openai.api_key = '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'


# response = openai.Image.create(
#   prompt="a white siamese cat",
#   n=1,
#   size="1024x1024"
# )
# image_url = response['data'][0]['url']


# response = openai.Image

# import required libraries
import cv2
import numpy as np

# Read an input image as a gray image
img = cv2.imread('car.jpg')

# create a mask
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:250, 150:450] = 255

# compute the bitwise AND using the mask
masked_img = cv2.bitwise_and(img,img,mask = mask)

# display the mask, and the output image
cv2.imshow('Mask',mask)
cv2.waitKey(0)
cv2.imshow('Masked Image',masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()