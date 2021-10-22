from flask import render_template
from app import db
from app.errors import bp


# For a custom designed error handler
@bp.app_errorhandler(404)
def not_found_error(error):

    # return an html template and an error status code
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    # reset the database session to prevent failed database sessions from
    # affecting the database
    db.session.rollback()

    # return an html template and an error status code
    return render_template('errors/500.html'), 500
