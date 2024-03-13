import streamlit as st
from PIL import Image
from PlatePerfect_2.main_2 import predict_with_pipeline_and_calories

def main():
    # Set the title and description
    st.title('Welcome to Plate Perfect!')
    st.write('Calorie tracking made easy - simple Food Image Recognition to keep track of your diet.! 😄')
    st.write('Please upload your food image and enter the serving size below!')

    uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    serving_size_grams = st.number_input("Enter serving size in grams", min_value=1, value=150)

    if uploaded_files:
        # blob & client aber anstatt download mach upload


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
