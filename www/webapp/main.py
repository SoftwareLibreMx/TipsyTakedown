from flask import Blueprint, render_template

from .modules.materials import materials_router
from .modules.course import course_router

webapp = Blueprint('web', __name__)

webapp.register_blueprint(materials_router, url_prefix='/material')
webapp.register_blueprint(course_router, url_prefix='/course')


@webapp.route('/')
def index():
    return render_template("index.html")
