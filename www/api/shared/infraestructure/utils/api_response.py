from flask import Response


def api_response(*args, **kwargs):
    return Response(
        *args,
        status=kwargs.get('status', 200),
        mimetype=kwargs.get('mimetype', 'application/json'))
