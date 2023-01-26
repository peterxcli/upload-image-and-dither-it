from flask import Flask, request, render_template, url_for, send_from_directory
import os
from PIL import Image
from dither import floydDither
import json
import uuid

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
if not os.path.exists('static/upload'): os.mkdir('static/upload')

# 判斷副檔名是否在 ALLOWED_EXTENSIONS 中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # 取得上傳檔案的清單
    files = request.files.getlist('file[]')
    image_urls = []
    images = []
    # 迭代每個檔案
    for file in files:
        if file and allowed_file(file.filename):
            # 從檔案中開啟圖片
            image = Image.open(file)
            # 對圖片進行Floyd-Steinberg演算法的抖動
            dithered_image = floydDither(image)
            # 從 numpy array 轉回 PIL image
            dithered_image = Image.fromarray(dithered_image)
        # 將原始檔案名稱和副檔名分開
        file_name, file_ext = os.path.splitext(file.filename)
        # 加入一個隨機的 UUID
        file_name += "_" + str(uuid.uuid1())
        # 儲存圖片
        dithered_image.save(os.path.join('static/upload', 'dithered_' + file_name + ".bmp"), format="bmp")
        # 將圖片複製到 images list 中
        images.append(dithered_image.copy())
        # 為圖片建立 url
        image_urls.append(url_for('image_file', filename='dithered_' + file_name + ".bmp"))
    # 回傳所有圖片的URL，200 OK，並設定Content-Type為application/json
    return json.dumps(image_urls), 200, {'ContentType':'application/json'}


@app.route('/static/upload/<path:filename>')
def image_file(filename):
    # 透過 filename 參數從 'static/upload' 資料夾中獲取圖片並返回
    return send_from_directory('static/upload', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
