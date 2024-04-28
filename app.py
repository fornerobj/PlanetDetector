from os import pread
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

from prediction_utils import predict_image

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            img_path = 'uploads/' + secure_filename(uploaded_file.filename)
            uploaded_file.save(img_path)
            print(predict_image(img_path))
    return render_template("index.html") 

if __name__ == "__main__":
    app.run()
