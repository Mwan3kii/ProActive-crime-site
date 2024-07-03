from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Flask, session
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db
from werkzeug.utils import secure_filename
import os
import uuid

UPLOAD_FOLDER = os.path.join("website","static","uploads")

views = Blueprint("views", __name__)

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif', 'webp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", user=current_user, posts=posts)

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        text1 = request.form.get('text1')
        uploaded_img = request.files.get("uploaded_img")

        if not text or not text1:
            flash('Post cannot be empty', category='error')
        elif uploaded_img and not allowed_file(uploaded_img.filename):
            flash('Not an image!(Accepted Formats -> png, jpg, jpeg, gif, webp)', category='error')
        else:
            if uploaded_img and allowed_file(uploaded_img.filename):
                picName = str(uuid.uuid1()) + os.path.splitext(uploaded_img.filename)[1]
                img_filename = secure_filename(picName)
                uploaded_img.save(os.path.join(UPLOAD_FOLDER, img_filename))
            else:
                picName = "proac_1.png"

            if current_user.is_authenticated:
                author_id = current_user.id
            else:
                author_id = 1  # Default user ID for anonymous posts

            post = Post(text=text, image=picName, title=text1, author=author_id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        text = request.form.get('text')
        text1 = request.form.get('text1')
        uploaded_img = request.files.get("uploaded_img")

        if not text or not text1:
            flash('Post cannot be empty', category='error')
        elif uploaded_img and not allowed_file(uploaded_img.filename):
            flash('Not an image!(Accepted Formats -> png, jpg, jpeg, gif, webp)', category='error')
        else:
            post.text = text
            post.title = text1
            if uploaded_img:
                picName = str(uuid.uuid1()) + os.path.splitext(uploaded_img.filename)[1]
                img_filename = secure_filename(picName)
                uploaded_img.save(os.path.join(UPLOAD_FOLDER, img_filename))
                post.image = picName

            db.session.commit()
            flash('Post updated!', category='success')
            return redirect(url_for('views.home'))

    return render_template('update_post.html', user=current_user, post=post)

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/'+ filename), code=301)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})
