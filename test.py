from flask import Flask, request, render_template, url_for, send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
from PIL import Image
from dither import floyd_steinberg_dither
import json
import uuid

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('upload.html')


# @app.route('/upload', methods=['POST'])
# def upload():
#     uploaded_files = request.files.getlist("file[]")
#     if not any(f for f in uploaded_files):
#         return redirect(url_for('index'))
#     file_details = []
#     for file in uploaded_files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             file_details.append([filename, text])

#     return render_template('display.html', files=file_details)

@app.route('/upload', methods=['POST'])
def upload_image():
    files = request.files.getlist('file[]')
    # print(files)
    # return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    image_urls = []
    images = []
    for file in files:
        if file and allowed_file(file.filename):
            image = Image.open(file)
            dithered_image = floyd_steinberg_dither(image)
        file_name, file_ext = os.path.splitext(file.filename)
        file_name += "_" + str(uuid.uuid1())
        dithered_image.save(os.path.join(
            'static/upload', 'dithered_' + file_name + ".bmp"), format="bmp")
        images.append(dithered_image.copy())
        image_urls.append(url_for('image_file', filename='dithered_' + file_name + ".bmp"))
    print(image_urls)
    return json.dumps(image_urls), 200, {'ContentType':'application/json'} 
    return render_template('show_image.html', image_urls=image_urls)


@app.route('/static/upload/<path:filename>')
def image_file(filename):
    return send_from_directory('static/upload', filename)

if __name__ == '__main__':
    app.run()
