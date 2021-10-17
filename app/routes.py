# This is use for the routes and logic of the web app
from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm
from datetime import datetime

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
                "section": "Science",
                "title": "Why do we drink the milk of animals instead of our own?",
                "author": "curious_impostor_2012",
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
                "date": now
            }
    ]

    # Render the index page
    return render_template("index.html", post=post, user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():

    # This is the form class from the forms.py
    form = LoginForm()

    # if the fields in the form have been validated
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('index'))

    # else render the html
    return render_template("login.html", user=user, form=form)


@app.route("/profile")
def profile():
    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    return redirect("/")


@app.route("/<section>")
def sections(section):

    # Check if section exists, if it does render that section page
    if section in SECTION:
        return render_template(f'{section}.html', user=user)
    return render_template("todo.html")


@app.route("/<section>/<int:thread_id>", methods=["GET", "POST"])
def thread(section, thread_id):

    # Check if thread exists
    if thread_id:
        return render_template(section + ".html", thread_id=thread_id,
                               user=user)
    return render_template("todo.html")
