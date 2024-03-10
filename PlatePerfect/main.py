# hugging face transfer learning model
from transformers import pipeline
import requests
import json

# Load the image classification pipeline with the desired model
image_classification_pipe = pipeline("image-classification", model="aspis/swin-finetuned-food101", from_pt=True)


# CalorieNinjas API endpoint
CALORIE_NINJAS_API_URL = "https://api.calorieninjas.com/v1/nutrition"


# API key for accessing CalorieNinjas API
API_KEY = "w210jDXcjkPMbH1kJaOKoA==S8t1b5l9MvkPhZkQ"



def get_calories(food):
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(f"{CALORIE_NINJAS_API_URL}?query={food}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def predict_with_pipeline_and_calories(image_paths):
    """
    Function to make predictions using the image classification pipeline for multiple images and retrieve nutritional information.

    Args:
    - image_paths: A list of paths to the image files.

    Returns:
    - predictions_with_calories: A list of dictionaries containing predictions and corresponding nutritional information for each image.
    """
    predictions_with_calories = []
    for image_path in image_paths:
        # Make prediction using the image classification pipeline
        prediction = image_classification_pipe(image_path)[0]  # Assuming only one prediction per image

        # Get nutritional information using the predicted food label
        nutritional_info = get_calories(prediction['label'])

        # Combine prediction and nutritional information
        prediction_with_calories = {
            'label': prediction['label'],
            'score': prediction['score'],
            'calories': nutritional_info
        }

        predictions_with_calories.append(prediction_with_calories)
    return predictions_with_calories
