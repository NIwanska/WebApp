from sqlalchemy import event
from sqlalchemy.orm import Session
from .models import ShoppingCart, CartItem, db

@event.listens_for(Session, 'after_flush')
def update_cart_total(session, flush_context):
    for instance in session.new:
        if isinstance(instance, CartItem):
            update_cart_total_amount(session, instance.shopping_cart_id)
    for instance in session.deleted:
        if isinstance(instance, CartItem):
            update_cart_total_amount(session, instance.shopping_cart_id)

def update_cart_total_amount(session, cart_id):
    cart = session.query(ShoppingCart).filter_by(id=cart_id).first()
    if cart:
        total = sum(item.quantity * item.product_item.product_type.price for item in cart.cart_item)
        cart.total = total
        session.add(cart)
