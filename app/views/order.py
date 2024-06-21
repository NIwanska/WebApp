from flask import render_template, Blueprint, request, flash, redirect
from ..models import Address, db, ShoppingCart, Order, AuthUser, DeliveryMethod, CartItem, ProductItem
from flask_login import login_required, current_user
import datetime
from ..utils.order_utils import get_saved_address_list, create_new_cart

bp = Blueprint(
    "order",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/order",
)


@bp.route("/")
@login_required
def index():
    saved_address_list = get_saved_address_list(current_user.id)
    delivery_methods = db.session.query(DeliveryMethod).all()
    return render_template(
        "order/make_order.html",
        saved_address_list=saved_address_list,
        delivery_methods=delivery_methods,
    )


@bp.route("/submit_order", methods=["POST"])
@login_required
def submit_order():
    if not request.form.get("use_saved_address", None) == "on":
        street = request.form["street"]
        city = request.form["city"]
        country = request.form["country"]
        zip_code = request.form["zip_code"]

        if not all([street, city, country, zip_code]):
            flash("All address fields are required!")
            return redirect("/order")

        address = Address(street=street, city=city, country=country, zip_code=zip_code)

        db.session.add(address)
        db.session.commit()
    else:
        address_id = request.form["saved_address_select"]
        address = Address.query.filter_by(id=address_id).first()

    cart = (
        ShoppingCart.query.filter_by(auth_user_id=current_user.id)
        .order_by(ShoppingCart.timestamp.desc())
        .first()
    )

    if cart.total is None:
        flash("Your cart is empty!")
        return redirect("/cart")
    
    # Check if any items in the cart are out of stock
    cart_items = CartItem.query.filter_by(shopping_cart_id=cart.id).all()
    out_of_stock_items = []
    for item in cart_items:
        product_item = ProductItem.query.filter_by(id=item.product_item_id).first()
        if product_item.stock_number < item.quantity:
            out_of_stock_items.append(product_item)

    if out_of_stock_items:
        for product in out_of_stock_items:
            flash(f"Product {product.product_type.name} in size {product.size.name} is out of stock!", "danger")
        return redirect("/cart")

    delivery_method_id = request.form["delivery_method_id"]
    order_status_id = 1
    datetime_val = datetime.datetime.now()
    total = cart.total
    order = Order(
        address_id=address.id,
        cart_id=cart.id,
        total=total,
        datetime=datetime_val,
        order_status_id=order_status_id,
        delivery_method_id=delivery_method_id,
    )
    db.session.add(order)
    db.session.commit()
    create_new_cart(current_user.id)
    flash("Order successfull!")

    return redirect("/order/success")


@bp.route("/success", methods=["GET"])
@login_required
def success():
    return render_template("order/success.html")
