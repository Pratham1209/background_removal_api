import requests
from PIL import Image
from io import BytesIO
from rembg import remove

def fetch_image(image_url: str) -> Image:
    """Fetch an image from a URL and return as a PIL image."""
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
    """Remove background from the given image."""
    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PNG')
    output_image_data = remove(img_byte_array.getvalue())
    return Image.open(BytesIO(output_image_data))

