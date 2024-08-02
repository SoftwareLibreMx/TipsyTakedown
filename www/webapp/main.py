from flask import Blueprint, render_template, request

from .modules.course import course_router
from .modules.errors import error_router
from .modules.materials import materials_router
from .modules.video import video_router
from .modules.auth import oauth_router

webapp = Blueprint('web', __name__)

webapp.register_blueprint(course_router, url_prefix='/course')
webapp.register_blueprint(error_router, url_prefix='/error')
webapp.register_blueprint(materials_router, url_prefix='/material')
webapp.register_blueprint(video_router, url_prefix='/video')
webapp.register_blueprint(oauth_router, url_prefix='/auth')


@webapp.route('/')
def index():
    return render_template("index.html")

@webapp.route('/client_callback')
def client_callback():
    token = request.args.get('token')
    return render_template('client_callback.html', token=token)