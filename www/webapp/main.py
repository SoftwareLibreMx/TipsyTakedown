from flask import Blueprint, render_template

from .modules.admin import admin_router
from .modules.auth import oauth_router
from .modules.errors import error_router
from .modules.video import video_router

webapp = Blueprint('web', __name__)

webapp.register_blueprint(admin_router, url_prefix='/admin')
webapp.register_blueprint(oauth_router, url_prefix='/auth')
webapp.register_blueprint(error_router, url_prefix='/error')
webapp.register_blueprint(video_router, url_prefix='/video')


@webapp.route('/')
def index():
    return render_template("index.html")


@webapp.route('/register')
def register():
    return render_template("register.html")

@webapp.route('/signup_signin')
def signup():
    return render_template("auth/login.html")