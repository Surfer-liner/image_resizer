# Image Resizing Application

This is a Django application that allows you to resize images. It provides an API for uploading images and obtaining resized copies with specified size parameters.

## Installation and Setup

1. Install Python and Django if you haven't already.
2. Clone the repository or download the application as a ZIP archive.
3. Navigate to the root directory of the project.
4. Install the dependencies by running the following command:

`pip install -r requirements.txt`
5. Apply migrations to create the necessary database tables:

`python manage.py migrate`

6. Start the Django development server:

`python manage.py runserver`
7. The application will be accessible at 
[http://localhost:8000/](http://localhost:8000/).

## Using the API

### Uploading an Image and Resizing

**URL:** `/api/resize/`

**Method:** `POST`

**Request Parameters:**
- `width` (required) - the width of the resized image.
- `height` (optional) - the height of the resized image. If not provided, the height will be set equal to the width.

**Response:**
- If the image is successfully resized, the response will contain the URL of the resized image.
- If there is an error, the response will contain an error message.

## Logging

The application logs informational messages and errors to a log file named `image_hub.log`. The log file is located in the base directory of the project.

## Additional Information

- The application uses the Python Imaging Library (PIL) to resize images.
- Resized images are saved in the `resized_images` directory within the media directory.

