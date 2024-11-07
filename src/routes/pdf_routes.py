from flask import Blueprint, request, jsonify
from services.vectore_store_service import initialize_vector_store
from services.vectore_store_service import process_and_store_file
from config import Config
from services.file_service import create_upload_folder
from services.file_service import save_file
from utils import allowed_file

pdf_routes = Blueprint('pdf_routes', __name__)
vector_store = initialize_vector_store()


@pdf_routes.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413


@pdf_routes.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload, validation, saving, and processing.
    This function processes file uploads via an HTTP POST request. It performs the following steps:
    1. Checks if a file is included in the request.
    2. Validates that the filename is not empty.
    3. Verifies that the file has an allowed extension.
    4. Creates the upload folder if it doesn't exist.
    5. Saves the uploaded file to the server.
    6. Processes the file and stores the result.
    7. Returns a JSON response indicating success or failure.
    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
    Responses:
        - 200 OK: File uploaded and processed successfully.
        - 400 Bad Request: Missing file part, no selected file, or invalid file extension.
        - 500 Internal Server Error: An error occurred during file processing.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename.strip()):
        try:
            create_upload_folder()
            filepath = save_file(file)
            process_and_store_file(filepath, vector_store)
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file extension'}), 400
