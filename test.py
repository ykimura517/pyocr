import pytesseract
from PIL import Image
import sys

img_path = sys.argv[1]
img = Image.open(img_path)

number = pytesseract.image_to_string(img)

print(number)

# see https://qiita.com/yoshi_yast/items/bd5e1e91ac9f64157203
