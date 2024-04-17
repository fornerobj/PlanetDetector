from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print("post method")
    return render_template("index.html") 

if __name__ == "__main__":
    app.run()
