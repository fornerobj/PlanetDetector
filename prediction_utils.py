# from keras.models import load_model
# from keras.preprocessing import image
import numpy as np
import tensorflow as tf

# model = load_model('my_model.keras')
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

planet_names = ['Earth', 'Jupiter', 'MakeMake', 'Mars', 'Mercury', 'Moon', 'Neptune', 'Pluto', 'Saturn', 'Uranus', 'Venus']

def predict_image(img_path):
    # img = image.load_img(img_path, target_size=(200, 200))
    # img_tensor = image.img_to_array(img)  # (height, width, channels)
    # img_tensor = np.expand_dims(img_tensor, axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    # img_tensor /= 255.  # imshow expects values in the range [0, 1]
    #
    # prediction = model.predict(img_tensor)
    # # Get the index of the maximum predicted value
    # predicted_planet_index = np.argmax(prediction)
    # # Get the corresponding planet name
    # predicted_planet_name = planet_names[predicted_planet_index]
    # return predicted_planet_name
    try: 
        img = tf.io.read_file(img_path)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.resize(img, [200, 200])
        img = tf.cast(img, tf.float32) / 255.0

        input_data = np.expand_dims(img, axis=0)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])

        predicted_planet_index = np.argmax(output_data)
        predicted_planet_name = planet_names[predicted_planet_index]
        return predicted_planet_name
    except Exception as e:
        print("Error: ", e)
        return "An error occurred. Possibly invalid file type"
