from flask import Blueprint, render_template

from ...libs.utils.language import get_translations
TEMPLATE_DIR = "auth"

auth_router = Blueprint("auth", __name__)


@auth_router.route("/login")
def login():
    return render_template(f"{TEMPLATE_DIR}/login.html",
                           translations=get_translations('login'))
