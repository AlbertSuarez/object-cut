import connexion

from flask_cors import CORS


# Setup (connexion-wrapped) Flask app
options = {'swagger_ui': False, 'serve_spec': True}
connexion_app = connexion.FlaskApp(__name__, specification_dir='./openapi/', options=options)

# Get native Flask object
flask_app = connexion_app.app
flask_app.config['JSON_AS_ASCII'] = False  # Needed for proper UTF-8 support
connexion_app.add_api('openapi.yaml', arguments={'title': 'ObjectCut API'})

# Setup CORS
CORS(flask_app)


@flask_app.route('/stillalive')
def health_check():
    return dict(message='API is hella working!')
