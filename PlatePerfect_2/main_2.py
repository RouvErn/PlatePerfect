from transformers import pipeline
import requests
import os

# Load the image classification pipeline with the desired model
image_classification_pipe = pipeline("image-classification", model="aspis/swin-finetuned-food101")

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

def predict_with_pipeline_and_calories(image_url, serving_size_grams=None):
    # predictions_with_calories = []
    # for img in image_data:
    #     prediction = image_classification_pipe(img)[0]
    #     nutritional_info = get_calories(prediction['label'], serving_size_grams)
    #     prediction_with_calories = {
    #         'label': prediction['label'],
    #         'score': prediction['score'],
    #         'calories': nutritional_info
    #     }
    #     predictions_with_calories.append(prediction_with_calories)
    prediction = image_classification_pipe(image_url)[0]
    nutritional_info = get_calories(prediction['label'], serving_size_grams)

    prediction_with_calories = {
        'label': prediction['label'],
        'score': prediction['score'],
        'calories': nutritional_info
    }

    return prediction_with_calories
