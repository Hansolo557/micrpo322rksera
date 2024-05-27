from pytesseract import pytesseract
import urllib.request
import cv2
import numpy as np

def extract(image_url):

    path_to_tesseract = r"PATH TO TESSERACT FOLDER"

    req = urllib.request.urlopen(image_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    pytesseract.tesseract_cmd = path_to_tesseract

    text = pytesseract.image_to_string(img)

    res = text[:-1]
    return res