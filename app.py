from flask import Flask, render_template, request
#from werkzeug import secure_filename
import os
import sys
from PIL import Image
import pytesseract
import argparse
import cv2
import pdftotext

__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      
      filename = f.filename

      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)
      
      if filename[-3:] == 'pdf':
          with open(filepath, "rb") as f:
            pdf = pdftotext.PDF(f)
          text = "\n\n".join(pdf)
      else:
          # load the example image and convert it to grayscale
          image = cv2.imread(filepath)
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          
          # apply thresholding to preprocess the image
          gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

          # apply median blurring to remove any blurring
          gray = cv2.medianBlur(gray, 3)

          # save the processed image in the /static/uploads directory
          ofilename = os.path.join(app.config['UPLOAD_FOLDER'],"{}.png".format(os.getpid()))
          cv2.imwrite(ofilename, gray)
          
          # perform OCR on the processed image
          text = pytesseract.image_to_string(Image.open(ofilename))
          
          # remove the processed image
          os.remove(ofilename)

      return render_template("uploaded.html", displaytext=text, fname=filename)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True)
