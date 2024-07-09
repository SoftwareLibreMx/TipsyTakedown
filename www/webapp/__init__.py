from flask import Blueprint, render_template

webapp = Blueprint('web', __name__)


@webapp.route('/')
def index():
    return render_template("index.html")
