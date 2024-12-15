import streamlit as st
from PIL import Image
from io import BytesIO
from rembg import remove
import requests
import boto3
import os
import uuid

# Initialize AWS credentials from Streamlit secrets
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
AWS_BUCKET_NAME = st.secrets["AWS_BUCKET_NAME"]
AWS_REGION = st.secrets["AWS_REGION"]

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# Image Processing Functions
def fetch_image(image_url: str) -> Image:
    """Fetch an image from a URL and return it as a PIL image."""
    response = requests.get(image_url)
    return Image.open(BytesIO(response.content))

def crop_image(image: Image, bounding_box: dict) -> Image:
    """Crop the image based on the provided bounding box coordinates."""
    return image.crop((
        int(bounding_box["x_min"]),
        int(bounding_box["y_min"]),
        int(bounding_box["x_max"]),
        int(bounding_box["y_max"])
    ))

def remove_background(image: Image) -> Image:
    """Remove the background from the given image."""
    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PNG')
    output_image_data = remove(img_byte_array.getvalue())
    return Image.open(BytesIO(output_image_data))

def upload_to_s3(image: Image, file_name: str) -> str:
    """Upload the processed image to S3 and return the public URL."""
    # Save the image to a temporary file
    temp_file_path = f"/tmp/{file_name}"
    image.save(temp_file_path, format="PNG")

    # Upload to S3
    s3_client.upload_file(
        temp_file_path, AWS_BUCKET_NAME, file_name, ExtraArgs={"ContentType": "image/png"}
    )

    # Generate the S3 public URL
    public_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"

    # Remove the local temporary file
    os.remove(temp_file_path)

    return public_url

# Streamlit App
st.title("Image Background Remover and Cropper")
st.write("Upload an image or provide a URL, specify a bounding box, and remove the background.")

# Image Upload Section
image_source = st.radio("Select Image Source", ("Upload", "URL"))
image = None

if image_source == "Upload":
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
elif image_source == "URL":
    image_url = st.text_input("Enter Image URL")
    if image_url:
        try:
            image = fetch_image(image_url)
        except Exception as e:
            st.error(f"Error fetching image: {e}")

# Bounding Box Input
if image:
    st.image(image, caption="Original Image", use_column_width=True)
    st.write("Specify the bounding box to crop the image.")
    x_min = st.number_input("x_min", min_value=0, value=0)
    y_min = st.number_input("y_min", min_value=0, value=0)
    x_max = st.number_input("x_max", min_value=0, value=image.width)
    y_max = st.number_input("y_max", min_value=0, value=image.height)

    bounding_box = {
        "x_min": x_min,
        "y_min": y_min,
        "x_max": x_max,
        "y_max": y_max,
    }

    # Process Image
    if st.button("Process Image"):
        try:
            cropped_image = crop_image(image, bounding_box)
            st.image(cropped_image, caption="Cropped Image", use_column_width=True)

            # Remove background
            processed_image = remove_background(cropped_image)
            st.image(processed_image, caption="Background Removed", use_column_width=True)

            # Upload to S3
            file_name = f"{uuid.uuid4()}.png"
            processed_image_url = upload_to_s3(processed_image, file_name)

            st.success("Image processed successfully!")
            st.write("Processed Image URL:", processed_image_url)
        except Exception as e:
            st.error(f"Error processing image: {e}")
