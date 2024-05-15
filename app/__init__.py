from flask import Flask
from .config import Config
from .views import main, cart, products, order, auth
from .database import db
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    migrate = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Db created")

    login_manager.init_app(app)
    from .models import AuthUser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return AuthUser.query.get(int(user_id))

    app.register_blueprint(main.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(order.bp)

    return app
