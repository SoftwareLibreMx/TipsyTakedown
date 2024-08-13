from flask import Blueprint

from .subscription import subscription_api

payment_api = Blueprint('payment_api', __name__)

payment_api.register_blueprint(subscription_api, url_prefix='/subscription')
