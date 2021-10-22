# This is use for the routes and logic of the web app
from flask import render_template, redirect, flash, url_for, request
from app import db
from app.main.forms import PostForm, CommentForm
from datetime import datetime
from flask_login import current_user, login_required
from app.models import User, Post, Comment
from app.main import bp

SECTION = ["gaming", "other", "science", "technology", "tv_film"]

posts_per_page = 10
comments_per_page = 15

user = {}


@bp.route("/")
def index():

    # Get the current date
    now = datetime.now()
    now = now.replace(microsecond=0)

    post = []

    # Parts of the post the user can see while not opening the post
    for section in SECTION:
        recent_post = Post.query.filter_by(section=section).order_by(
                    Post.timestamp.desc()).first()
        if recent_post:
            post.append(recent_post)

    # Render the index page
    return render_template("index.html", post=post)


@bp.route("/user/<username>")
def user(username):

    if username:
        # Search the name of the username entered
        user = User.query.filter_by(username=username).first_or_404()

        page = request.args.get('page', 1, type=int)

        # Search for the posts created by that user
        posts = Post.query.filter_by(author=user).order_by(
                    Post.timestamp.desc()).paginate(page, posts_per_page,
                                                    False)

        # Navigation controls for pages
        next_url = url_for('main.user', page=posts.next_num,
                           username=username) \
            if posts.has_next else None
        prev_url = url_for('main.user', page=posts.prev_num,
                           username=username) \
            if posts.has_prev else None

        # Render the user's profile page
        return render_template('user.html', user=user,
                               posts=posts.items, next_url=next_url,
                               prev_url=prev_url)

    # Tell the user that the user cannot be found
    return render_template("errors/404.html"), 404


@bp.route("/user/<username>/comments")
def user_comments(username):

    if username:
        # Search the name of the username entered
        user = User.query.filter_by(username=username).first_or_404()

        page = request.args.get('page', 1, type=int)

        # Search for the posts created by that user
        comments = Comment.query.filter_by(author=user).order_by(
                    Comment.timestamp.desc()).paginate(page,
                                                       comments_per_page,
                                                       False)

        # Navigation controls for pages
        next_url = url_for('main.user_comments', page=comments.next_num,
                           username=username) \
            if comments.has_next else None
        prev_url = url_for('main.user_comments', page=comments.prev_num,
                           username=username) \
            if comments.has_prev else None

        # Render the user's profile page
        return render_template('user_comments.html', user=user,
                               comments=comments.items, next_url=next_url,
                               prev_url=prev_url)

    # Tell the user that the user cannot be found
    return render_template("errors/404.html"), 404


@bp.route("/d/<section>", methods=["GET", "POST"])
def sections(section):

    # Check if section exists, if it does render that section page
    if section in SECTION:
        page = request.args.get('page', 1, type=int)

        # Query for the posts and get number of pages
        posts = Post.query.filter_by(section=section).order_by(
                Post.timestamp.desc()).paginate(page, posts_per_page,
                                                False)

        # Navigation controls for pages
        next_url = url_for('main.sections', page=posts.next_num,
                           section=section) \
            if posts.has_next else None
        prev_url = url_for('main.sections', page=posts.prev_num,
                           section=section) \
            if posts.has_prev else None

        # render the html page
        return render_template(f'{section}.html', section=section,
                               posts=posts.items, next_url=next_url,
                               prev_url=prev_url)

    # Else render page not found
    return render_template("errors/404.html"), 404


@bp.route("/d/<section>/<int:post_id>", methods=["GET", "POST"])
def post(post_id, section):

    # Check if post exists
    if post_id:

        # Load the post
        post = Post.query.filter_by(id=post_id).first_or_404()

        # Query for the comments and get number of pages
        page = request.args.get('page', 1, type=int)
        comments = Comment.query.filter_by(post_id=post.id).order_by(
                Comment.timestamp.asc()).paginate(page, comments_per_page,
                                                  False)

        # Navigation controls for pages
        next_url = url_for('main.post', page=comments.next_num,
                           section=section,
                           post_id=post_id) \
            if comments.has_next else None
        prev_url = url_for('main.post', page=comments.prev_num,
                           section=section,
                           post_id=post_id) \
            if comments.has_prev else None

        # render the html page
        return render_template("post.html", post=post, section=section,
                               comments=comments.items,
                               next_url=next_url, prev_url=prev_url,
                               post_id=post_id)

    # Else render "the page not found" page
    return render_template("errors/404.html"), 404


@bp.route("/d/<section>/<int:post_id>/<int:comment_id>",
          methods=["GET", "POST"])
def comment(post_id, comment_id, section):

    # Check if post exists
    if comment_id:

        # Load the post
        comment = Comment.query.filter_by(id=comment_id).first_or_404()

        # Query for the comments and get number of pages
        page = request.args.get('page', 1, type=int)
        replies = Comment.query.filter_by(parent_id=comment.id).order_by(
                Comment.timestamp.asc()).paginate(page, comments_per_page,
                                                  False)

        # Navigation controls for pages
        next_url = url_for('main.comment', page=replies.next_num,
                           section=section,
                           post_id=post_id,
                           comment_id=comment_id) \
            if replies.has_next else None
        prev_url = url_for('main.comment', page=replies.prev_num,
                           section=section,
                           post_id=post_id,
                           comment_id=comment_id) \
            if replies.has_prev else None

        # render the html page
        return render_template("comment.html", section=section,
                               replies=replies.items,
                               next_url=next_url, prev_url=prev_url,
                               comment_id=comment_id,
                               comment=comment)

    # Else render "the page not found" page
    return render_template("errors/404.html"), 404


@bp.route("/d/<section>/create-a-post", methods=["GET", "POST"])
@login_required
def create_a_post(section):

    # This is the form class from the forms.py that you will initialize
    form = PostForm()

    # If the user has submitted the form
    if form.validate_on_submit():

        # Add the post to the database
        post = Post(section=section,
                    title=form.title.data,
                    author=current_user,
                    description=form.description.data)
        db.session.add(post)
        db.session.commit()

        # Notify the user that post was submitted
        flash('Successfully Posted')

        # Send the user to their post
        return redirect(url_for('main.post', post_id=post.id,
                                section=section))

    # Else, render a webpage for the user to post
    return render_template('create.html', form=form, section=section)


@bp.route("/d/<section>/<int:post_id>/create-a-comment",
          methods=["GET", "POST"])
@login_required
def create_a_comment(section, post_id):

    # This is the form class from the forms.py that you will initialize
    form = CommentForm()

    # If the user has commented
    if form.validate_on_submit():

        post = Post.query.filter_by(id=post_id).first_or_404()

        # Add the comments of the post to the database
        comment = Comment(
                    author=current_user,
                    description=form.description.data,
                    post=post)
        db.session.add(comment)
        db.session.commit()

        # Notify the user that comment was submitted
        flash('Successfully Commented')

        # Send the user to the post
        return redirect(url_for('main.post', post=post,
                                section=section,
                                post_id=post_id))

    # Else, render a webpage for the user to post
    return render_template('create_comment.html', form=form,
                           section=section,
                           post=Post.query.filter_by(
                               id=post_id).first_or_404())


@bp.route("/d/<section>/<int:post_id>/<int:comment_id>/create-a-reply",
          methods=["GET", "POST"])
@login_required
def create_a_reply(section, post_id, comment_id):

    # This is the form class from the forms.py that you will initialize
    form = CommentForm()

    # If the user has commented
    if form.validate_on_submit():

        post = Post.query.filter_by(id=post_id).first_or_404()
        parent = Comment.query.filter_by(id=comment_id).first_or_404()

        # Add the comments of the post to the database
        comment = Comment(
                    author=current_user,
                    description=form.description.data,
                    post=post,
                    parent_id=parent.id)
        db.session.add(comment)
        db.session.commit()

        # Notify the user that comment was submitted
        flash('Successfully Commented')

        # Send the user to the comment
        return redirect(url_for('main.comment', comment=comment,
                                section=section,
                                post_id=post_id,
                                comment_id=comment_id))

    # Else, render a webpage for the user to post
    return render_template('create_reply.html', form=form, section=section,
                           post=Post.query.filter_by(
                               id=post_id).first_or_404(),
                           parent=Comment.query.filter_by(
                               id=comment_id).first_or_404())
