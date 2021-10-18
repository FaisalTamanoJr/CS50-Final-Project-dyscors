# This is use for the routes and logic of the web app
from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


SECTION = ["gaming", "other", "science", "technology", "tv_film"]

user = {}


@app.route("/")
def index():

    # Get the current date
    now = datetime.now()
    now = now.replace(microsecond=0)

    # Parts of the post the user can see while not opening the post
    post = [
            {
                "section": "Gaming",
                "title": "How to get better at Team Fortress 2?",
                "author": "Nabe Gewell",
                "date": now
            },
            {
                "section": "Other",
                "title": "Unpopular Opinion: kids should respect the elderly",
                "author": "John Farmer Dickinson",
                "date": now
            },
            {
                "section": "Technology",
                "title": "Rust sucks lol",
                "author": "C_masterrace",
                "date": now
            },
            {"section": "Television and Film",
                "title": "Is Breaking Bad still worth watching in 2021?",
                "author": "AsukaSoryu429",
                "date": now}
    ]

    # Render the index page
    return render_template("index.html", post=post, user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    # Redirect the user to the index if they are authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # This is the form class from the forms.py
    form = RegistrationForm()

    # If the user has submitted the form
    if form.validate_on_submit():

        # Register them to the database
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Tell the user that they successfully registered
        flash('User successfully registered')

        # Redirect them to the login screen
        return redirect(url_for('login'))

    # Else render the register html template
    return render_template('register.html', form=form, user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Redirect the user to the index if they are authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # This is the form class from the forms.py
    form = LoginForm()

    # If the user has submitted the form
    if form.validate_on_submit():

        # Search the user in the database based on the form
        user = User.query.filter_by(username=form.username.data).first()

        # If user does not exist on the database or the password is wrong
        if user is None or not user.check_password(form.password.data):

            # Tell the user that the username or password is invalid
            flash('The username or the password entered is invalid')

            # Redirect the user to the login page
            return redirect(url_for('login'))

        # Sign in the user
        login_user(user)

        # Redirect the user to the page they planned to go to earlier but were
        # required to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':

            # Else just redirect them to the index
            next_page = url_for('index')

        return redirect(next_page)

    # Else render the html template
    return render_template("login.html", user=current_user, form=form)


@app.route("/profile")
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/logout")
@login_required
def logout():

    # If the user is not signed in
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    # Else sign the user out
    logout_user()

    # Redirect the user to the index page
    return redirect(url_for('index'))


@app.route("/<section>", methods=["GET", "POST"])
def sections(section):

    # Check if section exists, if it does render that section page
    if section in SECTION:
        return render_template(f'{section}.html', user=current_user)
    return render_template("todo.html", user=current_user)


@app.route("/<section>/<int:post_id>", methods=["GET", "POST"])
def post(post_id):

    # Check if post exists
    if post_id:
        return render_template("post.html", post_id=post_id,
                               user=current_user)
    return render_template("todo.html", user=current_user)


@app.route("/<section>/<int:post_id>/<int:comment_id>",
           methods=["GET", "POST"])
def comment(post_id, comment_id):

    # Check if post exists
    if comment_id:
        return render_template("comment.html", post_id=post_id,
                               user=current_user, comment_id=comment_id)
    return render_template("todo.html", user=current_user)


@app.route("/<section>/create-a-post", methods=["GET", "POST"])
@login_required
def create_a_post():

    # If the method is post
    if request.method == "POST":
        print("ok")

    # Else, render a webpage for the user to post
    return render_template('create.html', user=current_user)
