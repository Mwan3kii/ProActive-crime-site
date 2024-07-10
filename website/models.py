"""Import necessary modules"""
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pytz
import datetime

# Define the User model, representing a user in the application.
class User(db.Model, UserMixin):
    """
    User model for storing user details.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): The email address of the user.
        username (str): The username chosen by the user.
        password (str): The hashed password of the user.
        role (str): The role assigned to the user.
        date_created (datetime): The date and time when user was created.
        post (relationship): Relationship to the Post model, representing posts created by the user.
        comments (reltionship): Relationship to the Comment model, representing comments mades by the user.
        likes (relationship): Relationship to the Like model, representing likes given by the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(80), default='user')
    date_created = db.Column(db.DateTime(pytz.timezone('Africa/Nairobi')), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)


# Define the Post model, representing a post created by user.
class Post(db.Model):
    """
    Post model for storing user posts.

    Attributes:
        id (int): Unique identifier for the post.
        text (str): The content of the post.
        title (str): The title of the post.
        image (str): The image associated with the post (optional).
        date_created (datetime): The date and time when the post was created.
        author (int): The ID of the user who created the post.
        comments (relationship): A relationship to the Comment model, representing the comments on the post.
        likes (relationship): A relationship to the Like model, representing the likes on the post.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)


# Define Comment model, representing a comment made on a post by a user.
class Comment(db.Model):
    """
    Comment model for storing comments on posts.

    Attributes:
        id (int): Unique identifier for the comment.
        text (str): The content of the comment.
        date_created (datetime): The date and time when the comment was created.
        author (int): The ID of the user who created the comment.
        post_id (int): The ID of the post that the comment is associated with.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)