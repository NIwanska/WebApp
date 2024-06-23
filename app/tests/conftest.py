import pytest
# import sys
# import os

# Add the root directory of the project to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from ..__init__ import create_app, db
from app.__init__ import *
# import __init__ as init
from app.models import (Size, SizeType, ProductType, ProductCategory, ProductItem, CartItem, ShoppingCart, AuthUser, 
                          Order, DeliveryMethod, OrderStatus, Address, Invoice, CityMonthlyReports, 
                          InvoiceMonthlyReports, ProductMonthlyReports)

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:'
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='session')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function', autouse=True)
def session(app):
    with app.app_context():

        connection = db.engine.connect()
        transaction = connection.begin()

        options = dict(bind=connection)
        session = db._make_scoped_session(options=options)

        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()

