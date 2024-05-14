import os
from flask import Flask, render_template, request
import tensorflow as tf
from keras.models import load_model
from tensorflow_hub import KerasLayer
from PIL import Image

app = Flask(__name__)


def predict_image_class(img_path, model, threshold=0.5):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(299, 299))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.expand_dims(img, 0)  # Create a batch
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    img = tf.image.convert_image_dtype(img, tf.float32)
    predictions = model.predict(img)
    score = predictions.squeeze()
    if score >= threshold:
        return f"This image is {100 * score:.2f}% malignant."
    else:
        return f"This image is {100 * (1 - score):.2f}% benign."


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_file = request.files.get('photo')

        if not uploaded_file:
            return "No file uploaded", 400

        try:
            # Save the uploaded file as "image.jpg"
            uploaded_file.save("image.jpg")

            custom_objects = {'KerasLayer': KerasLayer}
            model_path = 'SCD_model.h5'

            with tf.keras.utils.custom_object_scope(custom_objects):
                model = load_model(model_path)

            ans = predict_image_class("image.jpg", model)
            return render_template('index.html', result=ans)
        except Exception as e:
            return f"An error occurred: {e}", 400

    # Render the form page for GET requests or when the image is not uploaded yet
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
