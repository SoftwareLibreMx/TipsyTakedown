from flask import abort as flask_abort


def abort(status_code: int) -> None:
    flask_abort(status_code)
