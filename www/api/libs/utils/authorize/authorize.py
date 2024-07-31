from flask import g, request, redirect, url_for
from api.libs.domain_entity import UserType


def authorize(user_type_required: UserType):

# @authorize(UserType.ADMIN)from functools import wraps
	return None
	# def login_required(f):
	# 	@wraps(f)
	# 	def decorated_function(*args, **kwargs):
	# 		# add validation of the token
	# 		authorization_token = request.headers.get('Auhtorization', None)
	# 		# jwt TODO IMPLEMENT JWT 

	# 		# if 
	# 		if g.user is None:
	# 			return redirect(url_for('login', next=request.url))
	# 		return f(*args, **kwargs)
	# 	return decorated_function
	
	# return login_required