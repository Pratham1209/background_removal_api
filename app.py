import streamlit as st
from PIL import Image
from io import BytesIO
from rembg import remove
import boto3
import uuid
import os

# AWS Configuration
AWS_ACCESS_KEY = "your_aws_access_key"
AWS_SECRET_KEY = "your_aws_secret_key"
AWS_BUCKET_NAME = "your_s3_bucket_name"
AWS_REGION = "your_aws_region"

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# Image Processing Functions
def fetch_image(image_url: str) -> Image:
    """Fetch an image from a URL."""
    import requests
    response = requests.get(image_url)
    return Image.open(BytesIO(response.content))

def load_object_image() -> Image:
    """Load a default object image."""
    object_image_path = "path_to_object_image.png"  # Replace with actual path
    return Image.open(object_image_path)

def crop_image(image: Image, bounding_box: dict) -> Image:
    """Crop the image based on bounding box."""
    x_min, y_min, x_max, y_max = bounding_box.values()
    return image.crop((x_min, y_min, x_max, y_max))

def remove_background(image: Image) -> Image:
    """Remove background from an image."""
    img_byte_array = BytesIO()
    image.save(img_byte_array, format="PNG")
    output_data = remove(img_byte_array.getvalue())
    return Image.open(BytesIO(output_data))

def place_object(image: Image, object_image: Image, coords: tuple) -> Image:
    """Place the object image at specified coordinates on the input image."""
    x, y = coords
    object_image_resized = object_image.resize((100, 100))  # Adjust dimensions as needed
    if object_image_resized.mode != "RGBA":
        object_image_resized = object_image_resized.convert("RGBA")
    new_image = image.copy()
    new_image.paste(object_image_resized, (x, y), object_image_resized)
    return new_image

# Streamlit App
st.title("Image Processing App")
st.markdown("Upload an image or provide a URL to crop, remove the background, and overlay an object.")

# Input Options
image_source = st.radio("Select Image Source", ("Upload Image", "Image URL"))

# Image Upload or URL Input
if image_source == "Upload Image":
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        input_image = Image.open(uploaded_file)
elif image_source == "Image URL":
    image_url = st.text_input("Enter Image URL")
    if image_url:
        try:
            input_image = fetch_image(image_url)
        except Exception as e:
            st.error(f"Failed to fetch image: {e}")
            input_image = None
else:
    input_image = None

# Display Input Image
if input_image:
    st.image(input_image, caption="Input Image", use_column_width=True)

# Bounding Box Input
st.subheader("Bounding Box Parameters")
x_min = st.number_input("x_min", min_value=0, value=0)
y_min = st.number_input("y_min", min_value=0, value=0)
x_max = st.number_input("x_max", min_value=0, value=100)
y_max = st.number_input("y_max", min_value=0, value=100)

# Process Image Button
if st.button("Process Image") and input_image:
    try:
        # Load object image
        object_image = load_object_image()

        # Crop image
        cropped_image = crop_image(input_image, {"x_min": x_min, "y_min": y_min, "x_max": x_max, "y_max": y_max})

        # Remove background
        bg_removed_image = remove_background(cropped_image)

        # Place object image
        coords = (100, 100)
        final_image = place_object(bg_removed_image, object_image, coords)

        # Display Processed Image
        st.image(final_image, caption="Processed Image", use_column_width=True)

        # Save and Upload Processed Image to S3
        file_name = f"{uuid.uuid4()}.png"
        final_image.save(file_name, format="PNG")
        s3_client.upload_file(
            file_name, AWS_BUCKET_NAME, file_name, ExtraArgs={"ContentType": "image/png"}
        )
        processed_image_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        os.remove(file_name)

        # Display S3 URL
        st.success("Image processed successfully!")
        st.markdown(f"[Download Processed Image]({processed_image_url})")

    except Exception as e:
        st.error(f"Error processing image: {e}")
