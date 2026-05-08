from models.user import db, User
from models.task import Task
from flask_login import LoginManager

login_manager = LoginManager()

def init_models(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
