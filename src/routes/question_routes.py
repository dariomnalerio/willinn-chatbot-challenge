from flask import Blueprint, request, jsonify
from services.vectore_store_service import ask_question, initialize_vector_store

question_routes = Blueprint('question_routes', __name__)
vector_store = initialize_vector_store()


@question_routes.route('/', methods=['POST'])
def post_question():
    """
    Handles the POST request to submit a question.
    This function retrieves JSON data from the request, validates it, and processes the question
    using the `ask_question` function. It returns the response in JSON format.
    Returns:
      Response: A JSON response containing the answer to the question or an error message.
    Responses:
      - 200 OK: The question was processed successfully.
      - 400 Bad Request: The request is invalid or missing required data.
      - 500 Internal Server Error: An error occurred during question processing.
    """
    try:
        data = request.get_json()

        if not data or 'question' not in data:
            return jsonify({'error': 'Invalid request'}), 400

        response = ask_question(
            question=data['question'], vector_store=vector_store)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
