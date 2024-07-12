from flask import Blueprint, render_template

from .modules.materials import materials_router

webapp = Blueprint('web', __name__)

webapp.register_blueprint(materials_router, url_prefix='/material')


@webapp.route('/')
def index():
    return render_template("index.html")
