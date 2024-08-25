from flask import Blueprint, render_template

error_router = Blueprint('error', __name__)


@error_router.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404
