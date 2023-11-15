# Flask Audio API

This project is a simple Flask application that provides API endpoints for handling audio files. It includes basic authentication and supports uploading and retrieving audio files.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Atif999/audio-files.git

   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

1. Start the Flask application:

   ```bash
   python app.py run
   ```

   The application will be accessible at http://127.0.0.1:5000/.

## API Endpoints

- `GET /audio/<int:audio_id>`: Retrieve audio information in JSON format.
- `GET /audio/<int:audio_id>?file=true`: Retrieve audio information in file format.
- `POST /audio`: Upload an audio file.

## Running Tests

1. Run the unit tests:

   ```bash
   python test_api.py
   ```

   Ensure that the Flask application is not running while executing the tests.

## Notes

- The default authentication credentials for testing are:

  - Username: admin
  - Password: secret

Open Postman:
Open the Postman application on your computer. If you don't have Postman installed, you can download and install it from the official website.

Test POST Endpoint (Upload Audio):

Set up a new request in Postman.
Set the request type to POST.
Enter the URL: http://127.0.0.1:5000/audio.
In the request headers, add Authorization with the value Basic YWRtaW46c2VjcmV0 (this is the base64-encoded form of admin:secret).
Set the request body type to form-data.
Add a key named file with type File and select an audio file to upload.
Click "Send" to make the request.

Test GET Endpoint (Retrieve Audio):

Set up another request in Postman.
Set the request type to GET.
Enter the URL: http://127.0.0.1:5000/audio/1 (replace 1 with ID of the uploaded audio).
In the request headers, add Authorization with the value Basic YWRtaW46c2VjcmV0.
Click "Send" to make the request.
