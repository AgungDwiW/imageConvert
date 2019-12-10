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
from PIL import Image, ImageDraw, ImageFont
import base64

#nyoba2 auth
# from flask import Flask, abort, request, jsonify, g, url_for
# from flask_sqlalchemy import SQLAlchemy #
# from flask_httpauth import HTTPBasicAuth
# from passlib.apps import custom_app_context as pwd_context
# from itsdangerous import (TimedJSONWebSignatureSerializer
#                           as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
#.............
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# db = SQLAlchemy(app)
# auth = HTTPBasicAuth()


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(32), index=True)
#     password_hash = db.Column(db.String(64))
#
#     def hash_password(self, password):
#         self.password_hash = pwd_context.encrypt(password)
#
#     def verify_password(self, password):
#         return pwd_context.verify(password, self.password_hash)
#
#     def generate_auth_token(self, expiration=600):
#         s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
#         return s.dumps({'id': self.id})
#
#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None    # valid token, but expired
#         except BadSignature:
#             return None    # invalid token
#         user = User.query.get(data['id'])
#         return user
    #Regis

# @auth.verify_password
# def verify_password(username_or_token, password):
#     # coba pake token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # cek username/password
#         user = User.query.filter_by(username=username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from authModel import Auth

auth = Auth()

@app.route("/api/login", methods=['POST'])
def login():
    try:
        user = request.form.get("id")
        password = request.form.get("password")
    except:
        return jsonify(status='Error', message='arguments not satisfied')    
    return auth.login(user,password)

@app.route("/api/register", methods=['POST'])
def register():
    try:
        user = request.form.get("id")
        password = request.form.get("password")
        tipe = request.form.get("userType")
    except:
        return jsonify(status='Error', message='arguments not satisfied')    
    return auth.register(user,password, tipe)



@app.route("/api/scale", methods=['POST'])
def scale():
    """
    scale img to new size
    {“scale” : float, “token”: string, “image” : file, "ext" : string} 
    """
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'GET':
        return jsonify(status='OK', message='HI :)')
    else:
        """
        =====================
        check arguments
        ================================
        """
        try:
            scale = request.form.get('scale')
            token = request.form.get('token')
            file = request.files['image']
        except:
            return jsonify(status='Error', message='arguments not satisfied')    
        
        userId = auth.checkToken(token)
        """
        =====================
        check token / limit/ file
        ================================
        """
        if userId == False:
            return jsonify(status='Error', message='token is not valid')    
        if (auth.checkLimit(userId)):
            return jsonify(status='Error', message='Free limit has reached')
        
        if not (file and allowed_file(file.filename)):
            return jsonify(status='Bad Request', message='File not allowed')
        
        """
        =====================
        do the operation
        ================================
        """
        filename = secure_filename(file.filename)
        uploadpath = os.path.join('static/upload', datetime.now().strftime("%H%M%S") + filename)
        file.save(uploadpath)
        scale = float(scale)
        image = Image.open(uploadpath)
        height = image.height * scale
        width = image.height * scale
        size = (height, width)
        image.thumbnail(size, Image.ANTIALIAS)
        
        filenamedownload = datetime.now().strftime("%H%M%S") + '.' + ext
        downloadpath = os.path.join('static/download', filenamedownload)
        image.save(downloadpath)
        downloadlink = os.path.join(request.url_root, 'static/download', filenamedownload)
        """
        =====================
        updating the usage
        ================================
        """
        auth.updateUsage(userId, downloadlink)
        
        return jsonify(status='OK', message='berhasil', downloadlink=downloadlink)


# grayscale
# @app.route("/api/grayscale", methods=['POST'])
# def scale():
#     """
#     color to grayscale
#     {“greyscale” : int, “token”: string, “image” : file, "filename" : string} 
#     """
    
#     jsons = request.get_json()
#     try:
#         token = jsons['token']
#         ext = jsons['ext']
#         temp = secure_filename(ext)
#         file = open(temp, "wb")
#         file.write(base64.b64decode(jsons['image']))
#         files = open (temp, "rb")
#         image = Image.open(files)
        
#         os.remove(temp)
        
#         greyscale = jsons['greyscale']
        
#     except:
#         return json.dumps({'status':'error, argument not satisfied', "image": ""})

#     greyscaled = image.convert('LA')
#     size = (height, width)
#     a = secure_filename(ext)
#     image.thumbnail(size, Image.ANTIALIAS)
#     image.save(a, ext)
#     image = open(a, "rb")
#     image_data = image.read()
    
#     ENCODING = 'utf-8'
    
    
#     base64_bytes = base64.b64encode(image_data)
#     image_data = base64_bytes.decode(ENCODING)
    
#     ret = {"status": "success", "image": image_data}
    
#     ret = json.dumps(ret)
#     file.close()
#     files.close()
#     os.remove(a)
    
#     return ret


@app.route("/api/convert", methods=['GET', 'POST'])
def convert():
    """
        convert img to another ext
        {“ext” : float, “token”: string, “image” : file, "filename" : string}
    """

   
    if request.method == 'GET':
        return jsonify(status='OK', message='HI :)')
    else:
        
        """
        =====================
        check token / limit/ file
        ================================
        """
        file = request.files['image']
        token = request.form.get('token')
        userId = auth.checkToken(token)
        if userId == False:
            return jsonify(status='Error', message='token is not valid')    
        if (auth.checkLimit(userId)):
            return jsonify(status='Error', message='Free limit has reached')
        
        if not (file and allowed_file(file.filename)):
            return jsonify(status='Bad Request', message='File not allowed')

        

        if not (file and allowed_file(file.filename)):
            return jsonify(status='Bad Request', message='File not allowed')

        filename = secure_filename(file.filename)
        uploadpath = os.path.join('static/upload', datetime.now().strftime("%H%M%S") + filename)
        file.save(uploadpath)

        ext = request.form.get('ext')

        # Convert
        img = Image.open(uploadpath)
        img = img.convert("RGB")
        filenamedownload = datetime.now().strftime("%H%M%S") + '.' + ext
        downloadpath = os.path.join('static/download', filenamedownload)
        img.save(downloadpath)

        downloadlink = os.path.join(request.url_root, 'static/download', filenamedownload)

        return jsonify(status='OK', message='berhasil', downloadlink=downloadlink)

@app.route("/api/dont", methods=['GET', 'POST'])
def dont():
    """
        Do Nothing
        {“image” : file}
    """
    if request.method == 'GET':
        return jsonify(status='OK', message='HI :)')
    else:
        """
        =====================
        check token / limit/ file
        ================================
        """
        file = request.files['image']
        token = request.form.get('token')
        userId = auth.checkToken(token)
        if userId == False:
            return jsonify(status='Error', message='token is not valid')    
        if (auth.checkLimit(userId)):
            return jsonify(status='Error', message='Free limit has reached')
        
        if not (file and allowed_file(file.filename)):
            return jsonify(status='Bad Request', message='File not allowed')


        
        filename = secure_filename(file.filename)
        uploadpath = os.path.join('static/upload', datetime.now().strftime("%H%M%S") + filename)
        file.save(uploadpath)

        image = Image.open(uploadpath)

        #INCASE NOT MEMBER
        drawing = ImageDraw.Draw(image)

        black = (3, 8, 12)
        width, height = image.size
        text = 'FPKOMPUTASIAWAN'
        font = ImageFont.truetype("./arial.ttf", int(height / 15))
        w, h = drawing.textsize(text, font=font)
        pos = ((width - w) / 2, (height - h) / 2)
        drawing.text(pos, text, fill=black, font=font)
        #-------------------------
        downloadpath = os.path.join('static/download', datetime.now().strftime("%H%M%S") + filename)
        image.save(downloadpath)

        downloadlink = os.path.join(request.url_root, 'static/download', datetime.now().strftime("%H%M%S") + filename)

        return jsonify(status='OK', message='berhasil', downloadlink=downloadlink)

@app.route("/api/grey", methods=['GET', 'POST'])
def grey():
    """
        Do Nothing
        {“image” : file}
    """
    if request.method == 'GET':
        return jsonify(status='OK', message='HI :)')
    else:
        """
        =====================
        check token / limit/ file
        ================================
        """
        token = request.form.get('token')
        file = request.files['image']
        userId = auth.checkToken(token)
        if userId == False:
            return jsonify(status='Error', message='token is not valid')    
        if (auth.checkLimit(userId)):
            return jsonify(status='Error', message='Free limit has reached')
        
        if not (file and allowed_file(file.filename)):
            return jsonify(status='Bad Request', message='File not allowed')

        
        filename = secure_filename(file.filename)
        uploadpath = os.path.join('static/upload', datetime.now().strftime("%H%M%S") + filename)
        file.save(uploadpath)

        image = Image.open(uploadpath).convert('LA')
        image = image.convert('RGB')
        # in case not member
        drawing = ImageDraw.Draw(image)
        black = (3, 8, 12)
        width, height = image.size
        text = 'FPKOMPUTASIAWAN'
        font = ImageFont.truetype("./arial.ttf", int(height / 15))
        w, h = drawing.textsize(text, font=font)
        pos = ((width - w) / 2, (height - h) / 2)
        drawing.text(pos, text, font=font)

        downloadpath = os.path.join('static/download', datetime.now().strftime("%H%M%S") + filename)
        image.save(downloadpath)

        downloadlink = os.path.join(request.url_root, 'static/download', datetime.now().strftime("%H%M%S") + filename)

        return jsonify(status='OK', message='berhasil', downloadlink=downloadlink)

@app.route("/api/exif", methods=['GET', 'POST'])
def exif():
    """
        Do Nothing
        {“image” : file}
    """
    if request.method == 'GET':
        return jsonify(status='OK', message='HI :)')
    else:
        file = request.files['image']
        filename = secure_filename(file.filename)
        uploadpath = os.path.join('static/upload', datetime.now().strftime("%H%M%S") + filename)
        file.save(uploadpath)

        img = Image.open(uploadpath)
        print("path : "+uploadpath)
        img_exif = img.getexif()
        exif=[]
        if img_exif:
            print(type(img_exif))
            # <class 'PIL.Image.Exif'>
            print(dict(img_exif))
            # { .. 271: 'FUJIFILM', 305: 'Adobe Photoshop Lightroom 6.14 (Macintosh)', }

            img_exif_dict = dict(img_exif)
            for key, val in img_exif_dict.items():
                if key in ExifTags.TAGS:
                    exif.append(ExifTags.TAGS[key] + " - " + str(val))
        else:
            exif.append("Sorry, image has no exif data.")
        # print("exif_data")
        # print(exif_data)
        downloadpath = os.path.join('static/download', datetime.now().strftime("%H%M%S") + filename)
        img.save(downloadpath)

        # downloadlink = os.path.join(request.url_root, 'static/download', datetime.now().strftime("%H%M%S") + filename)

        return jsonify(status='OK', message='berhasil',exif=exif)


if __name__ == '__main__':
   app.run()
