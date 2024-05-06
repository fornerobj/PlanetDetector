import os, logging
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from werkzeug.utils import secure_filename

# Suppress TensorFlow info and warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = all messages are logged (default behavior), 1 = INFO messages are not printed, 2 = INFO and WARNING messages are not printed, 3 = INFO, WARNING, and ERROR messages are not printed

# Suppress warnings from other libraries
logging.getLogger("tensorflow").setLevel(logging.ERROR)

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
