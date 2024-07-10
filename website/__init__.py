"""Import necessary modules from Flask and other packages"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize SQLAlchemy database instance
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create and configure the Flask application
def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)

    # Configure the Flask app settings
    app.config['SECRET_KEY'] = "helloworld" # Secret key for session management and security
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Maximum content length for file uploads
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # SQLite database URI
    db.init_app(app) # Initialize SQLAlchemy with the app instance

    # Import and register blueprints for different parts of the application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import database models
    from .models import User, Post, Comment, Like

    # Create the database tables if they do not exist
    create_database(app)

    # Setup Flask-Login for managing user sessions
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Return the user object based on user ID

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database!")
