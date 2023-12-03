import requests
import numpy as np
import cv2 as cv
import os

from urllib.parse import urlparse
from image import cutter, badge


def save_images(poster_url, number, save_path):
    path = urlparse(poster_url).path
    file_name = os.path.basename(path)
    extension = os.path.splitext(file_name)[-1]

    poster_data = requests.get(poster_url).content
    buf = np.asarray(bytearray(poster_data), dtype="uint8")
    fanart = cv.imdecode(buf, cv.IMREAD_COLOR)

    poster_image = cutter.cut(fanart)
    poster = badge.tags(poster_image, number)
    thumbs = badge.tags(fanart, number)

    cv.imwrite(os.path.join(save_path, f"{number.file_name}-fanart{extension}"), fanart)
    cv.imwrite(os.path.join(save_path, f"{number.file_name}-poster{extension}"), poster)
    cv.imwrite(os.path.join(save_path, f"{number.file_name}-thumbs{extension}"), thumbs)

    return extension
