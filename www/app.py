import flask
# from authlib.integrations.flask_client import OAuth
from webapp import webapp
from api.shared.infraestructure.controller import api

# # Initialize OAuth
# oauth = OAuth()

def create_app():
    flask_app = flask.Flask(
        __name__,
        template_folder='webapp/templates',
        static_folder='webapp/static')

    # flask_app.config.from_mapping(
    #     SECRET_KEY='your_secret_key',
    #     OAUTH_CREDENTIALS={
    #         'google': {
    #             'client_id': 'your_google_client_id',
    #             'client_secret': 'your_google_client_secret',
    #         },
    #         'facebook': {
    #             'client_id': 'your_facebook_client_id',
    #             'client_secret': 'your_facebook_client_secret',
    #         }
    #     }
    # )

    # oauth.init_app(flask_app)


    @flask_app.route('/health')
    def health():
        return 'OK'

    flask_app.register_blueprint(webapp)
    flask_app.register_blueprint(api, url_prefix='/api/')

    return flask_app


flask_app = create_app()

if __name__ == '__main__':
    flask_app.run()
