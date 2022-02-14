import cv2
from stylize import render
# from scipy.misc import imread

image = cv2.imread('k.jpg')
defaults = render(image,ratio=0.001)
cv2.imwrite('o.jpg',defaults)