from flask import Flask, request, render_template, url_for, send_from_directory
import os
from PIL import Image
from dither import floyd_steinberg_dither

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        image_urls = []
        for file in files:
            if file and allowed_file(file.filename):
                image = Image.open(file)
                dithered_image = floyd_steinberg_dither(image)
            file_name, file_ext = os.path.splitext(file.filename)
            dithered_image.save(os.path.join('static/upload', 'dithered_' + file_name + ".bmp"), format="bmp")
            image_urls.append(url_for('image_file', filename='dithered_' + file_name + ".bmp"))
        print(image_urls)
        return render_template('show_image.html', image_urls=image_urls)
    else :
        print("fuck")
        return render_template('upload_image.html')

@app.route('/static/upload/<path:filename>')
def image_file(filename):
    return send_from_directory('static/upload', filename)

if __name__ == '__main__':
    app.run()


