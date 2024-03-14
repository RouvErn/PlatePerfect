import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from google.cloud import storage
from google.oauth2 import service_account
import json


# Define the FastAPI endpoint URL
API_URL = "https://plateperfect2-qo3jjoz2na-ew.a.run.app/predict" # Update with your FastAPI server URL
# API_URL = "http://localhost:8000/predict"
#"https://plateperfect2-qo3jjoz2na-ew.a.run.app/predict"

def predict_with_pipeline_and_calories(image_url, serving_size_grams):
    params = {'image_url': image_url, 'serving_size_grams': serving_size_grams}
    response = requests.get(API_URL, params=params) #data

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
        if uploaded_file:
            # service_account_info = json.load(open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))
            #credentials = service_account.Credentials.from_service_account_info(service_account_info)

            credentials = service_account.Credentials.from_service_account_file(
            '/Users/RouvenErnst/code/RouvErn/gcp/mineral-bonus-411314-3d34a7aa21e6.json'
            )

            client = storage.Client(credentials=credentials, project='plateperfect') #credentials=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
            bucket = client.get_bucket('plateperfect_public')

            blob = bucket.blob(uploaded_file.name)
            blob.upload_from_file(uploaded_file)

            # Open the uploaded file as an image
            #image = Image.open(uploaded_file)
            # Convert image to bytes
            #image_bytes = BytesIO()
            #image.save(image_bytes, format='JPEG')
            # Make prediction
            predictions = predict_with_pipeline_and_calories(blob.public_url, serving_size_grams)

            # Display predictions
            # for idx, (key, value) in enumerate(predictions.items()):
            #     st.subheader(f"Prediction {idx + 1}")
            #     st.write(f"Label: {predictions['label']}")
            #     st.write(f"Confidence Score: {predictions['score']:.2f}")
            #     st.write("Nutritional Information:")
            #     for item in predictions['calories']['items']:
            #         st.write(f"-  Type: {item['name']}")
            #         st.write(f"-  Calories: {item['calories']:.2f} kcal")
            #         st.write(f"-  Serving Size: {item['serving_size_g']} g")
            #         st.write(f"-  Fat: {item['fat_total_g']} g")
            #         st.write(f"-  Protein: {item['protein_g']} g")
            #         st.write(f"-  Carbohydrates: {item['carbohydrates_total_g']} g")
            #         st.write(f"-  Fiber: {item['fiber_g']} g")
            #         st.write(f"-  Sugar: {item['sugar_g']} g")
            st.subheader(f'Prediction')

            st.write(f"Label: {predictions['label']}")
            st.write(f"Confidence Score: {predictions['score']:.2f}")

            st.write("Nutritional Information:")
            for item in predictions['calories']['items']:
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
