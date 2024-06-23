import pytest
from flask import url_for
from app.models import AuthUser, ProductType, Size, ProductItem, ShoppingCart, CartItem, db
from app.views.auth import create_shopping_cart
from flask_login import login_user

def test_add_to_cart(test_client):
    with test_client:
        # Login as the test user
        user = AuthUser(id = 100000, username='testuser', password='password', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        create_shopping_cart(user_id=user.id)
        # user = AuthUser.query.filter_by(username='testuser').first()
        # login_user(user)

        product = ProductType.query.first()
        print(product)
        size = Size.query.first()
        print(size)

        # Test adding product to cart
        response = test_client.post(url_for('products.add_to_cart'), data={
            'product_id': product.id,
            'size': size.id,
            'quantity': 1
        }, follow_redirects=True)
        print(response)

        assert response.status_code == 200

        # Verify the product is in the cart
        cart = ShoppingCart.query.filter_by(auth_user_id=user.id).first()
        cart_item = CartItem.query.filter_by(shopping_cart_id=cart.id).first()
        assert cart.id is not None
        assert cart_item is not None
        assert cart_item.quantity == 1
        assert cart_item.product_item_id == ProductItem.query.filter_by(product_type_id=product.id, size_id=size.id).first().id

# def test_cart_detail(test_client):
#     with test_client:
#         # Login as the test user
#         user = AuthUser.query.filter_by(username='testuser').first()
#         login_user(user)

#         # Access the cart detail page
#         response = test_client.get(url_for('cart.cart_detail'))
#         assert response.status_code == 200
#         assert b'Cart' in response.data

#         # Verify cart details
#         cart = ShoppingCart.query.filter_by(auth_user_id=user.id).first()
#         assert cart is not None
#         assert b'T-shirt' in response.data
#         assert b'Medium' in response.data
#         assert b'19.99' in response.data

# def test_remove_from_cart(test_client):
#     with test_client:
#         # Login as the test user
#         user = AuthUser.query.filter_by(username='testuser').first()
#         login_user(user)

#         # Add a product to cart first
#         product = ProductType.query.first()
#         size = Size.query.first()
#         test_client.post(url_for('cart.add_to_cart'), data={
#             'product_id': product.id,
#             'size': size.id,
#             'quantity': 1
#         }, follow_redirects=True)

#         # Get the cart item id
#         cart = ShoppingCart.query.filter_by(auth_user_id=user.id).first()
#         cart_item = CartItem.query.filter_by(shopping_cart_id=cart.id).first()

#         # Test removing product from cart
#         response = test_client.post(url_for('cart.remove_from_cart'), data={
#             'cart_item_id': cart_item.id
#         }, follow_redirects=True)

#         assert response.status_code == 200
#         assert b'Product removed from cart' in response.data

#         # Verify the product is removed from the cart
#         cart_item = CartItem.query.filter_by(id=cart_item.id).first()
#         assert cart_item is None
