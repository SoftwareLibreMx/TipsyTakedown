GET '/'
GET '/health'
GET '/change_language/<language>'

GET 'admin/'
POST 'api/admin/course'
GET 'api/admin/course/<course_id>'
DELETE 'api/admin/course/<course_id>'
PUT 'api/admin/course/<course_id>'

GET 'api/admin/material'
GET 'api/admin/material/<material_id>'
POST 'api/admin/material/'
PATCH 'api/admin/material/<material_id>'
DELETE 'api/admin/material/<material_id>'

GET 'api/admin/lesson'
GET 'api/admin/lesson/<lesson_id>'

POST 'api/auth/sign_up'
POST 'api/auth/sign_in'
POST 'api/auth/check_email'


POST 'api/payment/'

GET 'api/subscription_type/<subscription_type_id>'
GET 'api/subscription_type/payment_cycles'
POST 'api/subscription_type'

GET 'checkout/'

GET "api/auth/sign_in"
POST "api/auth/sign_uo"
POST "api/auth/check_email"
GET "auth/logout"

GET "auth/google"
GET "auth/google/callback"

GET 'course/<course_id>/material/<material_id>'

