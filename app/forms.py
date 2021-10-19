from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User


# This is used for the variables of the login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# This is used for the variables of the registration form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
            "Confirm Password", validators=[DataRequired(),
                                            EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already taken')


# This is used for the variables of the post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Post Description",
                                validators=[Length(min=0, max=5000)])
    submit = SubmitField("Post")


# This is used for the variables of the comment form
class CommentForm(FlaskForm):
    description = TextAreaField("Comment", validators=[
                DataRequired(), Length(min=0, max=5000)])
    submit = SubmitField("Comment")
