from flask import render_template, Blueprint
from flask_login import login_required, current_user
from ..models import CartItem, ShoppingCart, db, ProductItem, ProductType, Size

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
    cart = ShoppingCart.query.filter_by(auth_user_id=current_user.id).order_by(ShoppingCart.timestamp.desc()).first()
    if cart is None:
        cart = ShoppingCart(auth_user_id=current_user.id, total=0)
        db.session.add(cart)
        db.session.commit()
    cart_items = (
        db.session.query(
            CartItem,
            CartItem.quantity,
            ProductType.name.label("product_name"),
            ProductType.price,
            ProductType.img_url,
            Size.name.label("size_name"),
        )
        .join(ProductItem, ProductItem.id == CartItem.product_item_id)
        .join(ProductType, ProductType.id == ProductItem.product_type_id)
        .join(Size, Size.id == ProductItem.size_id)
        .filter((CartItem.product_item_id == ProductItem.id) & (CartItem.shopping_cart_id == cart.id))
        .all()
    )
    return render_template("cart/cart_items_list.html", cart_items=cart_items, cart=cart)
