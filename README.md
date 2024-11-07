# Willinn Chatbot Challenge

## Overview

This project is a chatbot application that leverages FAISS for vector storage and retrieval, and integrates with a language model to answer questions based on the stored documents.

## Features

- **File Upload and Processing**: Upload PDF files, which are processed and stored in a FAISS vector store.
- **Question Answering**: Ask questions and get answers based on the content of the uploaded documents.


## Getting Started

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/willinn-chatbot-challenge.git
    cd willinn-chatbot-challenge
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Install [Ollama](https://ollama.com/)**:
   Ensure that Ollama is installed on your system

4. **Instal Required Models**:
    - **Embedding Model**: Install `nomic-embed-text` by running `ollama pull nomic-embed-text`
    - **LLM**: Install `llama3.2:1b` by running `ollama run llama3.2:1b`
5. **Run the application**:
    ```sh
    python src/app.py
    ```

## Usage

- **Upload a PDF**: Send a POST request to `/pdf/upload` with the file, using the name `file` for the form field.
- **Ask a Question**: Send a POST request to `/question` with key `question` and value as the question you want to ask.

## Configuration

- **`MAX_CONTENT_LENGTH`**: Maximum file size for uploads (16MB).
- **`UPLOAD_EXTENSIONS`**: Allowed file extensions for uploads (`pdf`).
- **`UPLOAD_PATH`**: Directory path for uploaded files (`db`).
- **`FAISS_DB_NAME`**: Directory name for the local FAISS storage (`faiss_db`).


## Project Architecture

The project is structured into several key directories to ensure modularity and maintainability:

### 1. **`app.py`**
   - The main entry point of the application. This script initializes the server, sets up routes, and starts the application. It brings together configurations, routes, and services to run the chatbot seamlessly.

### 2. **`config/`**
   - Contains configuration files for the application, such as settings for file uploads, FAISS storage paths, and integration with external models.

### 3. **`routes/`**
   - Handles all HTTP route definitions and request handling. This includes routes for file uploads (`/pdf/upload`) and question-answering (`/question`).

### 4. **`services/`**
   - Implements the core logic and functionalities of the application. This includes file processing, FAISS vector storage operations, and interactions with the language model for answering questions.

### 5. **`utils/`**
   - Contains utility functions and helper methods used across the project.
