# Background Removal API

This repository provides an API for removing the background from images using deep learning-based techniques. The application takes an image, processes it to remove the background, and returns the image with a transparent background.

## Table of Contents

- [Installation](#installation)
- [Running the Application Locally](#running-the-application-locally)
- [API Usage](#api-usage)
  - [Input](#input)
  - [Output](#output)
- [Libraries and Tools](#libraries-and-tools)
- [License](#license)

---

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Pratham1209/background_removal_api.git
    cd background-removal-api
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # For Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download Required Models (if applicable):**

    If your project requires a model for background removal (e.g., a deep learning model), make sure to download it from the provided link or repository and place it in the appropriate folder.

---

## Running the Application Locally

Once you have set up the environment and installed the dependencies, you can run the application locally using `uvicorn`.

### Run the API Server:

```bash
uvicorn app:app --reload

```

## API Usage

### Endpoint

- **POST** `/remove-background`

This endpoint receives an image and returns a version with the background removed.

### Input

The input must be a **JSON object** containing the following fields:

- `image_url` (string, required): URL of the image you want to process.  
  The image URL should be publicly accessible (e.g., a link to an image hosted on a public image hosting service).
  
#### Example Request Body:

```
```
json
{
  "image_url": "[https://example.com/your-image.png](https://plus.unsplash.com/premium_photo-1675186049563-000f7ac02c44?q=80&w=3087&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)"
}
## Output

The output will be a **JSON object** containing the URL to the image with the background removed.

### Example Response Body:

```
```
json
{
  "image_url": "[https://example.com/your-image-processed.png](https://image-processing-api-bucket.s3.us-east-1.amazonaws.com/6df0111b-4557-4ad9-adb6-d3f227041534.png)"
}
## Error Handling

### Missing required field:
If the required fields are missing, the API will return an error like this:

```
```
json
{
  "detail": "Field required"
}

```
```
### Postman Collection

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/33785306-d16069c2-06a8-42eb-b135-6f8274c184de?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D33785306-d16069c2-06a8-42eb-b135-6f8274c184de%26entityType%3Dcollection%26workspaceId%3D45dfb44a-9237-41be-9edd-bdba79abe8cd)

### Deployment Link

You can access the deployed application at the following link:

[Background Removal API](https://os--backgroundremovalapi.streamlit.app/)

### Deployed App 

# Input Interface
![image](https://github.com/user-attachments/assets/9623c46f-374d-4587-a790-56ca59161326)

# Input Image Preview
![image](https://github.com/user-attachments/assets/b0651f49-d1cb-440a-9bc0-c760bf282bfd)

# Input Parameters
![image](https://github.com/user-attachments/assets/337f9820-46aa-4c97-a929-a11aecad3d3a)

# Output Image with S3 Public Link

![image](https://github.com/user-attachments/assets/63a61225-8f59-46f3-9222-a2eab0080e2c)








 
