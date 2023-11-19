from flask import Flask
from flask_cors import CORS
from logging.config import dictConfig # For exporting logging file
from flask_ngrok import run_with_ngrok

from utils.config import *
from db import init_db, close_db
# from utils.database import Database
from modules.users.bp import bp as user_bp

def define_logging():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
            # Log file
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'file']
        },
    })

def create_app():
    # Define logging
    define_logging()

    # Create app
    app = Flask(__name__, instance_relative_config=True)
    run_with_ngrok(app)
    CORS(app)

    # Database
    init_db()
    app.teardown_appcontext(close_db)
    
    # Route/Blueprint here
    app.register_blueprint(user_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()