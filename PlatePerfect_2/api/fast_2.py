from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from PlatePerfect_2.main_2 import predict_with_pipeline_and_calories
from typing import List


app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/predict")
async def predict(image_files: List[UploadFile], serving_size_grams: int):
    """
    Endpoint to predict food items in images and retrieve nutritional information.
    Expects a list of uploaded image files and serving size in grams.
    """
    image_data = []
    for image_file in image_files:
        contents = await image_file.read()
        image = Image.open(BytesIO(contents))
        image_data.append(image)

    predictions_with_calories = predict_with_pipeline_and_calories(image_data, serving_size_grams)
    return predictions_with_calories

@app.get("/")
async def root():
    return {'greeting': 'Hello'}
