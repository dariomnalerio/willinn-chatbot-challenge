import os
from werkzeug.utils import secure_filename
from config import Config


def create_upload_folder():
    """
    Creates the upload directory specified in the configuration if it does not already exist.
    """
    if not os.path.exists(Config.UPLOAD_PATH):
        os.makedirs(Config.UPLOAD_PATH)


def save_file(file):
    """
    Saves an uploaded file to the configured upload path.
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_PATH, filename)

    file.save(filepath)

    return filepath
