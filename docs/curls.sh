
#!/bin/bash

# Environment variables
export HOST="http://localhost:8000"
export AUTH_TOKEN=""

# root
curl --location "$HOST/"

# health check
curl --location "$HOST/health"

# change language
curl --location "$HOST/change_language/en"

# curls for test
# Get JWT token
AUTH_TOKEN=$(curl --location "$HOST/api/auth/sign_in" \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "foo@foo.com",
    "password": "123123"
}'| jq -r '.token')

# Course - Get
curl --location --request GET "$HOST/api/admin/course/3192556e-e3d5-47c8-b8d3-68e9b814200b" \
	-H "Authorization: $AUTH_TOKEN"

# Course - Create
curl -X POST "$HOST/api/admin/course" \
     -H "Authorization: $AUTH_TOKEN" \
     -F "name=title1" \
     -F "description=short description" \
     -F "long_description=long description" \
     -F "thumbnail=@/Users/user/Downloads/FRASE.png"

# Course - Update
curl -X PUT "$HOST/api/admin/course/c78ae8f4-16ab-4518-976d-39d2cc483038" \
     -H "Authorization: $AUTH_TOKEN" \
     -F "name=title1" \
     -F "description=short description" \
     -F "long_description=long description" \
     -F "id=c78ae8f4-16ab-4518-976d-39d2cc483038" \
     -F "thumbnail=@/Users/user/Downloads/FRASE.png"

# Material - Get
curl --locationon "$HOST/api/admin/material/c376bb0a-67c9-47b4-8372-6ed4eaab2788" \
	-H "Authorization: $AUTH_TOKEN"

# Material - Create
curl --location "$HOST/api/admin/material/" \
	-H "Authorization: $AUTH_TOKEN" \
	-F 'teacher_id="e85f3cd0-b40b-4a3f-9867-79df7e60f4a9"' \
	-F 'material_type="PDF"' \
	-F 'name="foo"' \
	-F 'description="description"' \
	-F 'file=@"/Users/user/Downloads/dummy.pdf"'

# Material - Update
curl --location --request PATCH "$HOST/api/admin/material/c376bb0a-67c9-47b4-8372-6ed4eaab2788" \
	-H "Authorization: $AUTH_TOKEN" \
	-F 'teacher_id="e85f3cd0-b40b-4a3f-9867-79df7e60f4a9"' \
	-F 'material_type="PDF"' \
	-F 'name="foo"' \
	-F 'description="description"' \
	-F 'file=@"/Users/user/Downloads/dummy.pdf"'

# Material - Search
curl --location "$HOST/api/admin/material?query=foo" \
	-H "Authorization: $AUTH_TOKEN"

# Material - Delete
curl --location --request DELETE "$HOST/api/admin/material/c376bb0a-67c9-47b4-8372-6ed4eaab2788" \
	-H "Authorization: $AUTH_TOKEN"

# Lesson - Get all
curl --location "$HOST/api/admin/lesson" \
	-H "Authorization: $AUTH_TOKEN"

# Lesson - Get
curl --location "$HOST/api/admin/lesson/c376bb0a-67c9-47b4-8372-6ed4eaab2788" \
	-H "Authorization: $AUTH_TOKEN"

# Payments - Pay Subscription
curl -X POST "$HOST/api/payment/subscription" \
     -H "Authorization: $AUTH_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "subscription_type_id": "8361c656-a59c-4d71-81b8-0198278413a4",
           "payment_method": "CREDIT_CARD",
           "card": {
             "card_number": "5474925432670366",
             "expiration_date": "11/25",
             "cvv": "123",
             "card_holder_name": "APRO"
           }
         }'

# Subscription Type - Get
curl --location "$HOST/api/subscription_type/8361c656-a59c-4d71-81b8-0198278413a4" \
	-H "Authorization: $AUTH_TOKEN" 

# Subscription Type - post
curl --location "$HOST/api/subscription_type" \
    -H "Authorization: $AUTH_TOKEN" 
    -H 'Content-Type: application/json' \
--data-raw '{
    "name": "foo",
    "payment_cycle":"MONTHLY",
    "price":200.00,
    "currency":"MXN",
    "is_active": true
}'

# Checkout
curl --location "$HOST/checkout/?token=$AUTH_TOKEN"

# ADMIN
curl --location "http://localhost:8000/admin" \
	-H "Authorization: $AUTH_TOKEN"

# Auth - Sign Up
curl --location "$HOST/api/auth/sign_up" \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "foo@foo.com",
    "password": "123123",
    "given_name": "foo",
    "surname": "foo"
}'

# Auth - check email
curl --location "$HOST/api/auth/check_email" \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "foo@gmail.com"
}'

# Auth - Sign In
curl --location "$HOST/api/auth/sign_in" \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "foo@foo.com",
    "password": "123123"
}'

# Auth - Sign Out
curl --location 'http://localhost:8000/auth/logout' \
-H "Authorization: $AUTH_TOKEN" 

# Auth - Google
curl --location "$HOST/auth/google"

# Auth - Google Callback
curl --location "$HOST/auth/google/callback?state=R5e7sBbptGImiv9wyqXjqCJYWHH1dY&code=4%2F0AeanS0aVr41Cq72eJvN2iglGA2U4u2CoEEaTvmsTDeNfauJoRYGS1ACYqR2Ysl876_wBxg&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&authuser=0&prompt=none"