GET '/'
GET '/health'
GET '/change_language/<language>'

POST 'admin/course'
GET 'admin/course/<course_id>'
PUT 'admin/course/<course_id>'

GET 'admin/lesson'
GET 'admin/lesson/<lesson_id>'

GET 'admin/material'
GET 'admin/material/<material_id>'
POST 'admin/material/'
PATCH 'admin/material/<material_id>'
DELETE 'admin/material/<material_id>'

POST 'auth/sign_up'
POST 'auth/sign_in'
POST 'auth/check_email'

POST 'course/'
GET 'course/'

POST 'material/'
GET 'material/'

POST 'payment/'

GET 'subscription_type/<subscription_type_id>'
GET 'subscription_type/'

GET 'admin_router/'
GET 'admin_router/course/new'
GET 'admin_router/course/<course_id>/edit'
GET 'admin_router/video/uploader'

GET "auth/login"
GET "auth/logout"

GET "auth/google/"
GET "auth/google/callback"

GET 'checkout/'

GET 'course/<course_id>/material/<material_id>'

GET 'video/<video_id>'
