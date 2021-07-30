
from PIL import Image
import pytesseract
from flask import Flask, request, jsonify
from waitress import serve 

app = Flask(__name__)

@app.route("/image",  methods=['GET', 'POST'])
def ocr_core():
    file = request.files['file']

    text = pytesseract.image_to_string(Image.open(file))  
    return jsonify({"TExt":text})


if __name__ == '__main__':
        serve(app, port=82)





try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):

    text = pytesseract.image_to_string(Image.open(filename)) 
    return text

print(ocr_core('./test_image.jpeg'))
