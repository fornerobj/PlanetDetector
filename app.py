from os import pread
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from werkzeug.utils import secure_filename

from prediction_utils import predict_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/", methods=['POST', 'GET'])
def index():
    prediction = None
    filename = None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            img_path = 'uploads/' + secure_filename(uploaded_file.filename)
            uploaded_file.save(img_path)
            prediction = predict_image(img_path)
            filename = uploaded_file.filename
    return render_template("index.html", prediction=prediction, filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run()
