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

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()  # Assumes you have a `testing` config
    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()

        # Create a test user
        user = AuthUser(username='testuser', password='password', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        yield testing_client  # this is where the testing happens!

        db.drop_all()
        db.session.remove()

# @pytest.fixture(scope='module')
# def init_database():
#     # Initialize the database with some data
#     with create_app().app_context():
#         db.create_all()

#         # Create necessary objects for testing
#         size_type = SizeType(name='Clothing')
#         db.session.add(size_type)
#         db.session.commit()

#         size = Size(name='Medium', size_type_id=size_type.id)
#         db.session.add(size)
#         db.session.commit()

#         category = ProductCategory(subcategory_name='Shirts', category_name='Clothing', size_type_id=size_type.id)
#         db.session.add(category)
#         db.session.commit()

#         product_type = ProductType(name='T-shirt', color='Red', price=19.99, img_url='http://example.com/tshirt.png', product_category_id=category.id)
#         db.session.add(product_type)
#         db.session.commit()

#         product_item = ProductItem(stock_number=10, size_id=size.id, product_type_id=product_type.id)
#         db.session.add(product_item)
#         db.session.commit()

#         db.session.commit()
#         yield db

#         db.drop_all()
