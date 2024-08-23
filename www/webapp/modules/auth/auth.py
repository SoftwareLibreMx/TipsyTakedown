from flask import Blueprint, render_template

TEMPLATE_DIR = "auth"

auth_router = Blueprint("auth", __name__)


@auth_router.route("/login")
def login():
    return render_template(f"{TEMPLATE_DIR}/login.html")
