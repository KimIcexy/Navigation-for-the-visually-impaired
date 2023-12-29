from flask import Blueprint

from modules.users import bp as user_bp

bp = Blueprint('blueprint', __name__, url_prefix='/api/')
bp.register_blueprint(user_bp)