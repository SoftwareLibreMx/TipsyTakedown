from flask import Blueprint, render_template, redirect, session

from ...libs.utils.language import get_translations
from api.modules.payments.application.subscription_type import (
    subscription_type_application
)

TEMPLATE_DIR = "auth"
auth_router = Blueprint("auth", __name__)


@auth_router.route("/login")
def login():
    subscription_types = subscription_type_application.get_all()

    return render_template(f"{TEMPLATE_DIR}/login.html",
                           translations=get_translations('login'),
                           subscription_types=subscription_types)


@auth_router.route("/logout")
def logout():
    session.clear()

    return redirect('/')
