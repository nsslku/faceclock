import os
from stylize import render
from PIL import Image
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
# from scipy.misc import imread, imsave
# # pip install scipy==1.1.0
import imageio
from flask_cors import CORS
import imageio
from PIL import Image
import numpy as np
import cv2

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
cors = CORS(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/')
def hello_world():
    return 'Image Clock Whatch server'

@app.route("/upload4android", methods=['POST'])
def uploadAndConvert():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url), 200
        if file:
            filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = imageio.imread(UPLOAD_FOLDER + '/image.jpg')
        abstract = render(image, depth=6, verbose=True)
        imageio.imwrite('./static/image.jpg', abstract)
        background = cv2.imread('./static/image.jpg')
        overlay = cv2.imread('./static/foreground.png', -1)  # Load with transparency
        result = blend_transparent(background, overlay)
        cv2.imwrite('./static/image.jpg', result)
        image = Image.open('./static/image.jpg')
        image.show()
        return "http://localhost:5000/static/image.jpg", 200
        # return {"id": 1, "Username": "admin", "Level": "Administrator"}, 200
    return "http://localhost:5000/static/image.jpg", 200

@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        # f.save('./upload/%s' % secure_filename(fname))
        f.save('./upload/image.jpg')
        image = imageio.imread(UPLOAD_FOLDER + '/image.jpg')
        abstract = render(image, depth=6, verbose=True)
        imageio.imwrite('./static/image.jpg', abstract)
        background = cv2.imread('./static/image.jpg')
        overlay = cv2.imread('./static/foreground.png', -1)  # Load with transparency
        result = blend_transparent(background, overlay)
        cv2.imwrite('./static/image.jpg', result)
        image = Image.open('./static/image.jpg')
        # image.show()
        return "http://localhost:5000/static/image.jpg", 200
        # return {"id": 1, "Username": "admin", "Level": "Administrator"}, 200
    return "http://localhost:5000/static/image.jpg", 200
    # return 'Okay!'
@app.route("/api/enc", methods=['GET'])
def smoother():
    image = cv2.imread(UPLOAD_FOLDER + '/image.jpg')
    enc = render(image, iterations=25, verbose=True)  #сюда вставляется эффект
    imageio.imwrite('./static/image.jpg', enc)
    image = Image.open('./static/image.jpg')
    image.show()
    return "Complite encoding", 200
if __name__ == '__main__':
    app.run(host='0.0.0.0')
