from os import pread
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
app = Flask(__name__)
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

model = load_model('my_model.keras')
planet_names = ['Earth', 'Jupiter', 'MakeMake', 'Mars', 'Mercury', 'Moon', 'Neptune', 'Pluto', 'Saturn', 'Uranus', 'Venus']

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(200, 200))
    img_tensor = image.img_to_array(img)  # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.  # imshow expects values in the range [0, 1]

    prediction = model.predict(img_tensor)
    # Get the index of the maximum predicted value
    predicted_planet_index = np.argmax(prediction)
    # Get the corresponding planet name
    predicted_planet_name = planet_names[predicted_planet_index]
    return predicted_planet_name


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
