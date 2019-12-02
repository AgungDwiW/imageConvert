import datetime

from flask import Flask, request, jsonify, make_response, after_this_request
import json
import os
from flask import request
from os import remove
from werkzeug import secure_filename
from flask import Flask, redirect, url_for
from datetime import datetime
import json
from PIL import Image
import base64

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def checkToken(token):
    """
    check token; in progress
    """
    return True



@app.route("/api/scale", methods=['POST'])
def scale():
    """
    scale img to new size
    {“scale” : float, “token”: string, “image” : file, "filename" : string} 
    """
    
    jsons = request.get_json()
    try:
        token = jsons['token']
        ext = jsons['ext']
        temp = secure_filename(ext)
        file = open(temp, "wb")
        file.write(base64.b64decode(jsons['image']))
        files = open (temp, "rb")
        image = Image.open(files)
        os.remove(temp)
        
        scale = jsons['scale']
        
    except:
        return json.dumps({'status':'error, argument not satisfied', "image": ""})

    height = image.height * scale
    width = image.height * scale
    size = (height, width)
    a = secure_filename(ext)
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(a, ext)
    image = open(a, "rb")
    image_data = image.read()
    
    ENCODING = 'utf-8'
    
    
    base64_bytes = base64.b64encode(image_data)
    image_data = base64_bytes.decode(ENCODING)
    
    ret = {"status": "success", "image": image_data}
    
    ret = json.dumps(ret)
    file.close()
    files.close()
    os.remove(a)
    
    return ret

@app.route("/api/convert", methods=['GET', 'POST'])
def convert():
    """
        convert img to another ext
        {“ext” : float, “token”: string, “image” : file, "filename" : string}
        """

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'GET':
        return jsonify(status='OK', message='HI :)')
    else:
        file = request.files['image']

        if not (file and allowed_file(file.filename)):
            return jsonify(status='Bad Request', message='File not allowed')

        filename = secure_filename(file.filename)
        uploadpath = os.path.join('upload', datetime.now().strftime("%H%M%S") + filename)
        file.save(uploadpath)

        ext = request.form.get('ext')

        # Convert
        img = Image.open(uploadpath)
        img = img.convert("RGB")
        filenamedownload = datetime.now().strftime("%H%M%S") + '.' + ext
        downloadpath = os.path.join('download', filenamedownload)
        img.save(downloadpath)

        downloadlink = os.path.join(request.url_root, 'download', filenamedownload)

        return jsonify(status='OK', message='berhasil', downloadlink=downloadlink)


if __name__ == '__main__':
   app.run()
