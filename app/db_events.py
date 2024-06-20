from sqlalchemy import event
from sqlalchemy.orm import Session
from .models import ShoppingCart, CartItem, Order, Invoice
from sqlalchemy import text, bindparam
import datetime

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


@event.listens_for(Order, 'after_insert')
def create_invoice_after_order_insert(mapper, connection, target):
    connection.execute(
        Invoice.__table__.insert().values(
            total=target.total,
            order_id=target.id
        )
    )
    datetime_val = datetime.datetime.now()
    stmt_invoice = text("CALL invoice_reports(:p_month, :p_year, :p_total)")
    stmt_invoice = stmt_invoice.bindparams(
        # bindparam('p_month', value=str(datetime_val.month)),
        bindparam('p_month', value='7'),
        bindparam('p_year', value=datetime_val.year),
        bindparam('p_total', value=target.total)
    )
    connection.execute(stmt_invoice)
