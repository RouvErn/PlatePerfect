import streamlit as st
import requests


# Set the title and description
st.title('Welcome to Plate Perfect!')
st.write('Calorie tracking made easy - simple Food Image Recognition to keep track of your diet.')
st.write('Please enter the URL of your food image and the serving size below!')

# URL input for the image
image_url = st.text_input("Enter the URL of the food image")

# Serving size input
serving_size_grams = st.number_input("Enter the serving size in grams", min_value=0)

# Display the entered image URL as an image
if image_url:
    st.image(image_url, caption='Uploaded Image', use_column_width=True)

# Predict button
if st.button('Predict') and image_url:
    try:
        # API URL with placeholders filled
        api_url = f"https://plateperfect-qo3jjoz2na-ew.a.run.app/predict?image_paths={image_url}&serving_size_grams={serving_size_grams}"

        # Send a request to the API
        response = requests.get(api_url).json()

        # Assuming the response structure is as provided, extract information
        for item in response:
            st.write(f"**Label**: {item['label']}")
            st.write(f"**Confidence**: {item['score'] * 100:.2f}%")
            for food in item['calories']['items']:
                st.write(f"**Food Name**: {food['name']}")
                st.write(f"**Calories**: {food['calories']} kcal")
                st.write(f"**Serving Size**: {food['serving_size_g']} g")
                st.write(f"**Total Fat**: {food['fat_total_g']} g")
                st.write(f"**Saturated Fat**: {food['fat_saturated_g']} g")
                st.write(f"**Protein**: {food['protein_g']} g")
                st.write(f"**Sodium**: {food['sodium_mg']} mg")
                st.write(f"**Potassium**: {food['potassium_mg']} mg")
                st.write(f"**Cholesterol**: {food['cholesterol_mg']} mg")
                st.write(f"**Total Carbohydrates**: {food['carbohydrates_total_g']} g")
                st.write(f"**Dietary Fiber**: {food['fiber_g']} g")
                st.write(f"**Sugars**: {food['sugar_g']} g")

    except Exception as e:
        st.write("An error occurred:", e)
else:
    st.write("Please enter an image URL and the serving size to get a prediction.")
