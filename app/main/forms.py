from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


# This is used for the variables of the post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Post Description",
                                validators=[DataRequired(),
                                            Length(min=0, max=5000)])
    submit = SubmitField("Post")


# This is used for the variables of the comment form
class CommentForm(FlaskForm):
    description = TextAreaField("Comment", validators=[
                  Length(min=0, max=5000)])
    submit = SubmitField("Comment")
