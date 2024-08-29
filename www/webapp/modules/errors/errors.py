from flask import Blueprint, render_template

from ...libs.utils.language import get_translations
error_router = Blueprint('error', __name__)


@error_router.app_errorhandler(404)
def not_found(e):
    return render_template(
        'errors/404.html', translations=get_translations()), 404
