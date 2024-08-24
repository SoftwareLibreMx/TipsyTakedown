from flask import Blueprint

from api.modules.auth.infraestructure.controllers import auth_api
from api.modules.payments.infraestructure.controllers import payment_api

api = Blueprint('api', __name__)

api.register_blueprint(auth_api, url_prefix='/auth')
api.register_blueprint(payment_api, url_prefix='/payment')
