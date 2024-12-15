from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.image_processing import fetch_image, crop_image, remove_background
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME, AWS_REGION
import boto3
import uuid
import os

# Initialize FastAPI
app = FastAPI()

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


# Request and Response Models
class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class ImageRequest(BaseModel):
    image_url: str
    bounding_box: BoundingBox


class ImageResponse(BaseModel):
    original_image_url: str
    processed_image_url: str


@app.post("/remove-background", response_model=ImageResponse)
def remove_background_api(request: ImageRequest):
    try:
        # Fetch the main image
        image = fetch_image(request.image_url)

        # Crop the main image based on the provided bounding box
        cropped_image = crop_image(image, request.bounding_box.dict())

        # Remove the background from the cropped image
        processed_image = remove_background(cropped_image)

        # Define where to place the object image (coordinates are static for now)
        coords = (100, 100)  # Example coordinates, can be dynamic or adjuste

        # Generate a unique file name for the processed image
        file_name = f"{uuid.uuid4()}.png"

        # Save the processed image locally
        processed_image.save(file_name, format="PNG")

        # Upload the processed image to S3
        s3_client.upload_file(
            file_name, AWS_BUCKET_NAME, file_name, ExtraArgs={"ContentType": "image/png"}
        )

        # Generate the public URL for the uploaded image
        processed_image_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"

        # Remove the local file after upload to S3
        os.remove(file_name)

        return ImageResponse(
            original_image_url=request.image_url,
            processed_image_url=processed_image_url,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
