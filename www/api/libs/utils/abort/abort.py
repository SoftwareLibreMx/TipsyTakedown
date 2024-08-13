from flask import abort as flask_abort, make_response, jsonify


def abort(status_code: int, message: str) -> None:
    response = make_response(jsonify({'error': message}))
    response.status_code = status_code

    flask_abort(response)
