from flask import g, request, redirect, url_for, jsonify
from api.libs.domain_entity import UserType
from shared.tipsy_jwt import verify_token
from functools import wraps


def authorize(user_type_required: UserType):
	def login_required(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			# authorization_token = request.headers.get('Authorization', None)
			token = request.headers.get('Authorization').split()[1]
			verification_result = verify_token(token)
			if verification_result == 'Token has expired':
				return jsonify({'message': 'Token has expired'}), 401
			elif verification_result == 'Invalid token':
				return jsonify({'message': 'Invalid token'}), 401

			if verification_result is None:
				return redirect(url_for('login', next=request.url))
			return f(*args, **kwargs)
		return decorated_function
	return login_required