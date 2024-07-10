"""Initializes the main entry point of the Flask application"""
from website import create_app

# Check if this script is being run directly
if __name__ == "__main__":
    # Create an instance of the Flask application using create_app function
    app = create_app()
    app.run(debug=True)