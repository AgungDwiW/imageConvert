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
img = Image.open('28558.jpg')
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
print(exif)