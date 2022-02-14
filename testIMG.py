import os
from stylize import render
from PIL import Image
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
# from scipy.misc import imread, imsave
# # pip install scipy==1.1.0
import imageio
from PIL import Image
import numpy as np
import cv2

UPLOAD_FOLDER = './upload'

def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

if __name__ == '__main__':
    # image = cv2.imread(UPLOAD_FOLDER + '/image.jpg')
    image = imageio.imread(UPLOAD_FOLDER + '/image.jpg')
    # file.save(os.path.join('./static/image.jpg'))
    # cv2.imwrite('./static/image.jpg',image)
    # imageio.imwrite('./static/image.jpg', image)
    abstract = render(image, depth=6, verbose=True)
    # # smoother = render(image, iterations=35, verbose=True)
    # # aa = render(image, anti_aliasing=True, verbose=True)
    # # less_detail = render(image, ratio=0.001, verbose=True)
    # # more_detail = render(image, ratio=0.00005, verbose=True)
    # # landmarks = render(image, features='landmarks', verbose=True)
    # # defaults = render(image, verbose=True)
    # imageio.imwrite('./static/image.jpg', abstract)
    # imsave('./static/image.jpg', landmarks)
    # abstract = abstract.save('./static/image.jpg')
    # imsave(r'./static/image.jpg', abstract)
    # show_img(abstract, "A depth of 4 results in an abstract representation")
    imageio.imwrite('./static/image.jpg', abstract)

    # image = Image.open('./static/image.jpg')
    # image.save('./static/image.png')

    background = cv2.imread('./static/image.jpg')
    overlay = cv2.imread('./static/foreground.png', -1) # Load with transparency
    result = blend_transparent(background, overlay)
    cv2.imwrite('./static/image.jpg', result)

    image = Image.open('./static/image.jpg')
    image.show()
