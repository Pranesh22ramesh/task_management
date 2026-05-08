from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from config import Config
from models import db, init_models
from services.websocket_service import socketio
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
from routes.analytics_routes import analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    init_models(app)
    socketio.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(analytics_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, port=5000)
