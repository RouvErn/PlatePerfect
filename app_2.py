from transformers import pipeline
import requests
from PIL import Image
from io import BytesIO
import streamlit as st

# Load the image classification pipeline with the desired model
image_classification_pipe = pipeline("image-classification", model="aspis/swin-finetuned-food101")

def get_calories(food, serving_size_grams=None):
    url = "https://api.calorieninjas.com/v1/nutrition?query="
    headers = {
        'X-Api-Key': 'w210jDXcjkPMbH1kJaOKoA==S8t1b5l9MvkPhZkQ'
    }
    if serving_size_grams:
        query = f"{serving_size_grams}g {food}"
        url += query
    else:
        url += food
    response = requests.get(url, headers=headers).json()
    return response

def predict_with_pipeline_and_calories(image_data, serving_size_grams=None):
    predictions_with_calories = []
    for img in image_data:
        prediction = image_classification_pipe(img)[0]
        nutritional_info = get_calories(prediction['label'], serving_size_grams)
        prediction_with_calories = {
            'label': prediction['label'],
            'score': prediction['score'],
            'calories': nutritional_info
        }
        predictions_with_calories.append(prediction_with_calories)
    return predictions_with_calories

def main():
    st.title("Image Classifier with Calorie Estimation")

    uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    serving_size_grams = st.number_input("Enter serving size in grams", min_value=1, value=150)

    if uploaded_files:
        if st.button("Predict"):
            image_data = [Image.open(file) for file in uploaded_files]
            predictions_with_calories = predict_with_pipeline_and_calories(image_data, serving_size_grams)

            for idx, prediction in enumerate(predictions_with_calories):
                st.subheader(f"Prediction {idx + 1}")
                st.image(image_data[idx], caption=f"Predicted Label: {prediction['label']}")

                st.write(f"Confidence Score: {prediction['score']:.2f}")
                for item in prediction['calories']['items']:
                    st.write(f"- Type: {item['name']}")
                    st.write(f"  Calories: {item['calories']:.2f} kcal")
                    st.write(f"  Serving Size: {item['serving_size_g']} g")
                    st.write(f"  Fat: {item['fat_total_g']} g")
                    st.write(f"  Protein: {item['protein_g']} g")
                    st.write(f"  Carbohydrates: {item['carbohydrates_total_g']} g")
                    st.write(f"  Fiber: {item['fiber_g']} g")
                    st.write(f"  Sugar: {item['sugar_g']} g")


if __name__ == "__main__":
    main()
