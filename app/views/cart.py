from flask import render_template, Blueprint
from flask_login import login_required, current_user
from ..models import CartItem, ShoppingCart, db, Product, ProductType

bp = Blueprint(
    "cart",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/cart",
)


@bp.route("/")
@login_required
def cart_detail():
    cart = (
        ShoppingCart.query.filter_by(auth_user_id=current_user.id)
        .order_by(ShoppingCart.timestamp.desc())
        .first()
    )
    # cart_items = CartItem.query.filter_by(shopping_cart_id=cart.id).all()
    cart_items = (
        db.session.query(CartItem, Product.name, ProductType.price, ProductType.img_url)
        .join(Product, Product.id == CartItem.product_id)
        .join(ProductType, ProductType.id == Product.product_type_id)
        .filter(
            (CartItem.product_id == Product.id) & (CartItem.shopping_cart_id == cart.id)
        )
        .all()
    )
    return render_template(
        "cart/cart_items_list.html", cart_items=cart_items, cart=cart
    )
