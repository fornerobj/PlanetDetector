from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        image = request.files['file']
        image.save('uploads/' + secure_filename(image.filename))
    return render_template("index.html") 

if __name__ == "__main__":
    app.run()
