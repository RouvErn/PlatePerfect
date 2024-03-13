# hugging face transfer learning model
from transformers import pipeline
import requests
import os

# Load the image classification pipeline with the desired model
image_classification_pipe = pipeline("image-classification",model="aspis/swin-finetuned-food101" )
#model="aspis/swin-finetuned-food101"
#model="nateraw/food"

def get_calories(food, serving_size_grams=None):
    url = "https://api.calorieninjas.com/v1/nutrition?query="
    headers = {
        'X-Api-Key': os.environ['API_KEY']
    }
    if serving_size_grams:
        query = f"{serving_size_grams}g {food}"
        url += query
    else:
        url += food
    response = requests.get(url, headers=headers).json()
    return response


def predict_with_pipeline_and_calories(image_paths, serving_size_grams=None):
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
        nutritional_info = get_calories(prediction['label'], serving_size_grams)

        # Combine prediction and nutritional information
        prediction_with_calories = {
            'label': prediction['label'],
            'score': prediction['score'],
            'calories': nutritional_info
        }

        predictions_with_calories.append(prediction_with_calories)
    return predictions_with_calories
