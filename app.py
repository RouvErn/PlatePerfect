import streamlit as st
from PIL import Image
import os
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('food_classification_model.h5')


st.title('Plate Perfect!')
st.write('Hello and welcome to Plate perfect. Upload your food image below!')

# File uploader widget
uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])

def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((150, 150))  # Resize the image to match model input size
    img = np.asarray(img) / 255.0  # Normalize pixel values
    return img

# Function to make predictions
def predict(image):
    img = preprocess_image(image)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    prediction = model.predict(img)
    return prediction



# Display the uploaded image
if uploaded_file is not None:
    # You can use PIL or other libraries to read and process the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Make predictions
    prediction = predict(uploaded_file)
    st.write('Predicted class:', prediction)