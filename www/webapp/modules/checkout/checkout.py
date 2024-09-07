import urllib

from flask import Blueprint, render_template, request, redirect, session

from ...libs.utils.language import get_translations
from api.modules.payments.application.subscription_type import subscription_type_application

TEMPLATE_DIR = 'checkout'
checkout_router = Blueprint('checkout', __name__)


@checkout_router.route('/')
def index():
    session_token = session.get('token')
    token = request.args.get('token', session_token)

    session['token'] = token

    if not token:
        subscription_type = (
            f'?subscription_type_id={request.args.get("subscription_type_id")}'
            if request.args.get('subscription_type_id')
            else ''
        )
        parsed_url = urllib.parse.quote_plus(f'/checkout{subscription_type}')

        return redirect(f'/auth/login?redirect={parsed_url}')

    subscription_types = subscription_type_application.get_all()
    subscription_type_id = request.args.get('subscription_type_id')
    # Use the subscription_type_id as needed
    return render_template(f'{TEMPLATE_DIR}/index.html',
                           translations=get_translations(),
                           subscription_type_id=subscription_type_id,
                           subscription_types=subscription_types)
