from flask import Flask
"""
This module initializes and runs the Flask application.
"""
from routes.pdf_routes import pdf_routes
from routes.question_routes import question_routes
from config import Config


def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(pdf_routes, url_prefix='/pdf')
    app.register_blueprint(question_routes, url_prefix='/question')
    return app


app = create_app()

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}")
