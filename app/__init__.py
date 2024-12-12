from flask import Flask
from app.config import load_config
from app.services.redis_service import init_redis_client
from app.routes.health_records import health_records_bp

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.update(load_config())
    
    # Initialize Redis
    init_redis_client(app)
    
    # Register blueprints
    app.register_blueprint(health_records_bp)
    
    return app