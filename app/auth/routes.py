from flask import render_template, redirect, flash, url_for, request
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.auth import bp
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@bp.route("/login", methods=["GET", "POST"])
def login():

    # Redirect the user to the index if they are authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

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
            return redirect(url_for('auth.login'))

        # Sign in the user
        login_user(user)

        # Redirect the user to the page they planned to go to earlier but were
        # required to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':

            # Else just redirect them to the index
            next_page = url_for('main.index')

        return redirect(next_page)

    # Else render the html template
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    # Redirect the user to the index if they are authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

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
        return redirect(url_for('auth.login'))

    # Else render the register html template
    return render_template('auth/register.html', form=form)


@bp.route("/logout")
@login_required
def logout():

    # If the user is not signed in
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    # Else sign the user out
    logout_user()

    # Redirect the user to the index page
    return redirect(url_for('main.index'))
