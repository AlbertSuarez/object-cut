import connexion

from flask_cors import CORS


connexion_app = connexion.FlaskApp(__name__, specification_dir='./openapi/')
flask_app = connexion_app.app
flask_app.config['JSON_AS_ASCII'] = False
connexion_app.add_api('openapi.yaml', arguments={'title': 'ObjectCut API'})

CORS(flask_app)


@flask_app.route('/')
def alive_check():
    return 'Welcome to ObjectCut API!', 200
