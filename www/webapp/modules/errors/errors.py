from flask import Blueprint, render_template, redirect

from ...libs.utils.language import get_translations
error_router = Blueprint('error', __name__)


@error_router.app_errorhandler(404)
def not_found(e):
    return render_template(
        'errors/404.html', translations=get_translations()), 404


@error_router.app_errorhandler(401)
def unauthorized(e):
    return redirect('/auth/login')


@error_router.app_errorhandler(403)
def forbidden(e):
    return render_template(
        'errors/403.html', translations=get_translations()), 403
