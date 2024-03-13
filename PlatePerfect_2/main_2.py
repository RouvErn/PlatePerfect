from transformers import pipeline
import requests
import os

# Load the image classification pipeline with the desired model
image_classification_pipe = pipeline("image-classification", model="aspis/swin-finetuned-food101")

def get_calories(food, serving_size_grams=None):
    """
    Get nutritional information for a given food item.

    Args:
        food (str): The name of the food item.
        serving_size_grams (int, optional): The serving size in grams. Defaults to None.

    Returns:
        dict: Nutritional information for the food item.
    """
    url = "https://api.calorieninjas.com/v1/nutrition?query="
    headers = {
        'X-Api-Key': os.environ.get['API_KEY']  # Retrieving API key from environment variable
    }
    if serving_size_grams:
        query = f"{serving_size_grams}g {food}"
        url += query
    else:
        url += food
    response = requests.get(url, headers=headers).json()
    return response

def predict_with_pipeline_and_calories(image_data, serving_size_grams=None):
    """
    Predict labels for images and estimate calories for predicted food items.

    Args:
        image_data (list): List of PIL.Image objects representing images.
        serving_size_grams (int, optional): The serving size in grams. Defaults to None.

    Returns:
        list: List of dictionaries containing prediction labels, confidence scores, and nutritional information.
    """
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
