class Config:
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_EXTENSIONS = {'pdf'}
    UPLOAD_PATH = 'db'
    # Will also be used as the directory name for the local storage.
    FAISS_DB_NAME = 'faiss_db'
