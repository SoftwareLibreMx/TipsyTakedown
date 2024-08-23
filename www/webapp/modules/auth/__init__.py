from flask import Blueprint

from .auth import auth_router
from .google_oauth import google_oauth_router

oauth_router = Blueprint('oauth', __name__)

oauth_router.register_blueprint(auth_router, url_prefix='')
oauth_router.register_blueprint(google_oauth_router, url_prefix='/google')
