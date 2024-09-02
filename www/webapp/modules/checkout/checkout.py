from flask import Blueprint, render_template, request

from ...libs.utils.language import get_translations
from api.modules.payments.application.subscription_type import subscription_type_application

TEMPLATE_DIR = 'checkout'
checkout_router = Blueprint('checkout', __name__)


@checkout_router.route('/')
def index():
    subscription_types = subscription_type_application.get_all()
    subscription_type_id = request.args.get('subscription_type_id')
    # Use the subscription_type_id as needed
    return render_template(f'{TEMPLATE_DIR}/index.html',
                           translations=get_translations(),
                           subscription_type_id=subscription_type_id,
                           subscription_types=subscription_types)
