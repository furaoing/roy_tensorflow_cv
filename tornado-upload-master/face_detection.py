# -*- coding: utf-8 -*-

import facepp
import json
import config

from facepp import API
from facepp import File

API_KEY = config.API_key
API_SECRET = config.API_secret
API_URL = config.API_url


def face_detect(image_url):
    api = API(API_KEY, API_SECRET, API_URL)
    face = api.detection.detect(img = File(image_url))
    print(face)

    has_human_face = True if len(face["face"]) > 0 else False

    gender = face["face"][0]["attribute"]["gender"]["value"] if has_human_face else None

    if has_human_face:
        print("Contain Human Face")
        print("Gender: "+ gender)
    else:
        print("NO Human Face")

    return has_human_face, gender


if __name__ == "__main__":
    image_url = r"/home/furaoing/roy_tensorflow_cv/tornado-upload-master/uploads/8oaec4.jpg"
    face_detect(image_url)
