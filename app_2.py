import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Define the FastAPI endpoint URL
API_URL = "http://localhost:8000/predict"  # Update with your FastAPI server URL


def predict_with_pipeline_and_calories(image_bytes, serving_size_grams):
    files = {'image_files': ("image.jpg", image_bytes, "image/jpeg")}
    params = {'serving_size_grams': serving_size_grams}
    response = requests.post(API_URL, files=files, params=params) #data
    return response.json()


def main():
    # Set the title and description
    st.title('🥗 Welcome to Plate Perfect! 🥗')
    st.write('Calorie tracking made easy - Use our Food Image Recognition AI to keep track of your diet! 💪')
    st.write('---')

    st.write('Please upload an image of your meal and enter the serving size below! ☺️')


    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])

    serving_size_grams = st.number_input("Enter serving size in grams", min_value=1, value=150)

    if uploaded_file:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    if st.button("Predict"):
        if uploaded_file is not None:
            # Open the uploaded file as an image
            image = Image.open(uploaded_file)
            # Convert image to bytes
            image_bytes = BytesIO()
            image.save(image_bytes, format='JPEG')
            # Make prediction
            predictions = predict_with_pipeline_and_calories(image_bytes.getvalue(), serving_size_grams)

            print(predictions)

            # Display predictions
            for idx, prediction in enumerate(predictions):
                st.subheader(f"Prediction {idx + 1}")
                st.write(f"Label: {prediction['label']}")
                st.write(f"Confidence Score: {prediction['score']:.2f}")
                st.write("Nutritional Information:")
                for item in prediction['calories']['items']:
                    st.write(f"-  Type: {item['name']}")
                    st.write(f"-  Calories: {item['calories']:.2f} kcal")
                    st.write(f"-  Serving Size: {item['serving_size_g']} g")
                    st.write(f"-  Fat: {item['fat_total_g']} g")
                    st.write(f"-  Protein: {item['protein_g']} g")
                    st.write(f"-  Carbohydrates: {item['carbohydrates_total_g']} g")
                    st.write(f"-  Fiber: {item['fiber_g']} g")
                    st.write(f"-  Sugar: {item['sugar_g']} g")
        else:
            st.warning("Please upload an image before clicking predict.")


if __name__ == "__main__":
    main()
