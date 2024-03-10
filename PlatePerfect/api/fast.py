
import json
from fastapi import FastAPI
#from PlatePerfect.main import predict_with_pipeline_and_calories
from fastapi.middleware.cors import CORSMiddleware

from PlatePerfect.main import predict_with_pipeline_and_calories

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
async def predict(image_paths: str):
    """
    Endpoint to predict food items in images and retrieve nutritional information.
    Expects a comma-separated string of image paths.
    """
    image_paths_list = image_paths.split(',')
    predictions_with_calories = predict_with_pipeline_and_calories(image_paths_list)
    return predictions_with_calories


@app.get("/")
async def root():
    return {'greeting': 'Hello'}
