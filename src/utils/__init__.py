from config import Config


def allowed_file(filename):
    """
    Determine if a given filename has an allowed extension.
    Args:
        filename (str): The name of the file to check.
    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.UPLOAD_EXTENSIONS
