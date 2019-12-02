#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 05:51:05 2019

@author: temperantia
"""
from PIL import Image


image = open("udanLiris.jpg", "rb")
image = image.read()

import base64
ENCODING = 'utf-8'

base64_bytes = base64.b64encode(image)

# third: decode these bytes to text
# result: string (in utf-8)
base64_string = base64_bytes.decode(ENCODING)
image = base64_string
#{“scale” : float, “token”: string, “image” : file, "filename" : string}#
args = {"scale" : 0.5,
       "token": "REEEEEEE",
       "image" : image,
       "ext" : "jpeg"
       }

import requests

req = requests.post("http://127.0.0.1:5000/api/scale", json= args)

import json
json_resp = json.loads(req.content)
image_new = json_resp["image"]
image_new = base64.b64decode(image_new)

file = open("image_new.jpg", "wb")
file.write(image_new)
file.close()