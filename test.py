from flask import Flask, request, render_template, url_for, send_from_directory
import os
from PIL import Image
from dither import floydDither
import json
import uuid

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
if not os.path.exists('static/upload'): os.mkdir('static/upload')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    files = request.files.getlist('file[]')
    image_urls = []
    images = []
    for file in files:
        if file and allowed_file(file.filename):
            image = Image.open(file)
            # dithered_image = floyd_steinberg_dither(image)
            dithered_image = floydDither(image)
            dithered_image = Image.fromarray(dithered_image)
        file_name, file_ext = os.path.splitext(file.filename)
        file_name += "_" + str(uuid.uuid1())
        dithered_image.save(os.path.join(
            'static/upload', 'dithered_' + file_name + ".bmp"), format="bmp")
        images.append(dithered_image.copy())
        image_urls.append(url_for('image_file', filename='dithered_' + file_name + ".bmp"))
    print(image_urls)
    return json.dumps(image_urls), 200, {'ContentType':'application/json'}


@app.route('/static/upload/<path:filename>')
def image_file(filename):
    return send_from_directory('static/upload', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
