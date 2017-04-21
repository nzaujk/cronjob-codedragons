
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)
    Bootstrap(app)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    from app import models
    from app.admin import administrator
    app.register_blueprint(administrator, url_prefix='/admin')

    from app.auth import authenticate
    app.register_blueprint(authenticate)

    from app.home import home_blueprint
    app.register_blueprint(home_blueprint)

    from app.store.views import store_blueprint
    app.register_blueprint(store_blueprint)
    from app.product.views import product_blueprint
    app.register_blueprint(product_blueprint)

    return app
