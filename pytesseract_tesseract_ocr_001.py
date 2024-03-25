# _*_ coding:utf-8 _*_
import pytesseract as pt
from PIL import Image

path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pt.pytesseract.tesseract_cmd = path
img = Image.open(r"c:\users\ggg\desktop\jpgsample_005.jpg")
text = pt.image_to_string(img, lang="eng")
print(text)

# print(pt.image_to_data(img, lang="chi_tra"))
