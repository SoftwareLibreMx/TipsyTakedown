from flask import Blueprint, render_template

TEMPLATE_LOCATION = 'course/components/createCourse'
create_course_router = Blueprint('create_course', __name__)


@create_course_router.route('')
def create_wizard():
    return render_template(f'{TEMPLATE_LOCATION}/index.html')
