from flask import Flask,request,jsonify,make_response, after_this_request
import json
import os
from flask import request
from os import remove
from werkzeug import secure_filename
from flask import Flask, redirect, url_for
import json
from PIL import Image

app = Flask(__name__)

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
        image = Image.open(jsons['image'])
        scale = jsons['scale']
        ext = jsons['ext']
    except:
        return json.dumps({'status':'error, argument not satisfied', "image": ""})

    height = image.height * scale
    width = image.height * scale
    size = (height, width)
    a = secure_filename()
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(a, ext)
    image = open(a, "rb")
    ret = {"status": "success", "image": image}

    @after_this_request
    def remove_file(response):
        try:
            image.close()
            os.remove(a)
        except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
    return ret


if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('',5000),app)
    http_server.serve_forever()
