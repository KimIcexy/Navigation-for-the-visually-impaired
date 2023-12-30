from flask import Blueprint

from modules.users import bp as user_bp
from modules.obstacles import bp as obstacle_bp

bp = Blueprint('blueprint', __name__, url_prefix='/api/')
bp.register_blueprint(user_bp)
bp.register_blueprint(obstacle_bp)