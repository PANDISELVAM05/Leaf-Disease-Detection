import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'plant_disease_model.h5')
model = None

if os.path.exists(model_path):
    model = load_model(model_path)
    print("Model loaded successfully.")
else:
    print(f"Error: Model file '{model_path}' not found. Please check the file path.")

# Class labels
labels = {0: 'Healthy', 1: 'Powdery Mildew', 2: 'Rust'}

# Function to process and predict the image
def get_result(image_path):
    try:
        img = load_img(image_path, target_size=(225, 225))
        x = img_to_array(img)
        x = x.astype('float32') / 255.0  # Normalize the image
        x = np.expand_dims(x, axis=0)  # Expand dimensions for model input

        predictions = model.predict(x)[0]  # Get predictions
        predicted_label = labels[np.argmax(predictions)]  # Get the highest probability label
        return predicted_label
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Ensure the "uploads" directory exists
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze_disease', methods=['POST'])
def analyze_disease():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(f.filename))
    f.save(file_path)

    # Get prediction
    predicted_label = get_result(file_path)

    return jsonify({'prediction': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
