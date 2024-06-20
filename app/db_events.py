from sqlalchemy import event
from sqlalchemy.orm import Session
from .models import db, CartItem, ShoppingCart, ProductItem, ProductType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_cart_total_direct(connection, shopping_cart_id):
    cart = connection.execute(
        db.text("SELECT id FROM cart WHERE id = :cart_id"),
        {"cart_id": shopping_cart_id}
    ).fetchone()
    
    if cart:
        total = connection.execute(
            db.text("""
                SELECT SUM(ci.quantity * pt.price) as total
                FROM cart_item ci
                JOIN product_item pi ON ci.product_item_id = pi.id
                JOIN product_type pt ON pi.product_type_id = pt.id
                WHERE ci.shopping_cart_id = :cart_id
            """),
            {"cart_id": shopping_cart_id}
        ).scalar()
        
        connection.execute(
            db.text("UPDATE cart SET total = :total WHERE id = :cart_id"),
            {"total": total if total is not None else 0, "cart_id": shopping_cart_id}
        )
        logger.info(f"Updating cart_id {shopping_cart_id} total to {total}")


@event.listens_for(CartItem, 'after_insert')
@event.listens_for(CartItem, 'after_update')
@event.listens_for(CartItem, 'after_delete')
def after_cart_item_change(mapper, connection, target):
    update_cart_total_direct(connection, target.shopping_cart_id)
