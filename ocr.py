import easyocr as ocr
from PIL import Image


reader = ocr.Reader(['en'], gpu=True, model_storage_directory='.')

result = reader.readtext('bizcard.png')

for text in result:
    print(text[1])