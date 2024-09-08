from flask import Blueprint

from api.modules.admin.infrastructure.controllers.admin import admin_api
from api.modules.auth.infraestructure.controllers import auth_api
from api.modules.course.infrastructure.controllers import (
    course_api, material_api
)
from api.modules.payments.infraestructure.controllers import payment_api
from api.modules.payments.infraestructure.controllers.subscription_type import (
    subscription_type_api
)

api = Blueprint('api', __name__)

api.register_blueprint(admin_api, url_prefix='/admin')
api.register_blueprint(auth_api, url_prefix='/auth')
api.register_blueprint(course_api, url_prefix='/course')
api.register_blueprint(material_api, url_prefix='/material')
api.register_blueprint(payment_api, url_prefix='/payment')
api.register_blueprint(subscription_type_api, url_prefix='/subscription_type')
