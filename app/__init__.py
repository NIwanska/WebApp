from flask import Flask
from .config import Config
from .views import main, cart, products
from .database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Db created")

    app.register_blueprint(main.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(products.bp)

    return app
