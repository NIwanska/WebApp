from flask import render_template, Blueprint, request, flash, redirect
from ..models import Address, db, ShoppingCart, Order, AuthUser
from flask_login import login_required, current_user
import datetime

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
    # saved_address_list = Address.query.filter_by(user_id=current_user.id).all()
    saved_address_list = (
        db.session.query(Address)
        .join(Order, Address.id == Order.address_id)
        .join(ShoppingCart, ShoppingCart.id == Order.cart_id)
        .join(AuthUser, AuthUser.id == ShoppingCart.auth_user_id)
        .filter((AuthUser.id == current_user.id))
        .all()
    )
    return render_template(
        "order/make_order.html", saved_address_list=saved_address_list
    )


@bp.route("/submit_order", methods=["POST"])
@login_required
def submit_order():
    if not request.form.get("saved_address_select", None):
        street = request.form["street"]
        city = request.form["city"]
        country = request.form["country"]
        zip_code = request.form["zip_code"]

        address = Address(street=street, city=city, country=country, zip_code=zip_code)

        db.session.add(address)
        db.session.commit()

    cart = ShoppingCart.query.filter_by(auth_user_id=current_user.id).first()
    delivery_method_id = request.form["delivery_method_id"]
    order_status_id = 1
    datetime_val = datetime.datetime.utcnow()
    total = cart.total

    order = Order(
        address_id=address.id,
        cart_id=cart.id,
        total=total,
        datetime=datetime_val,
        order_status_id=order_status_id,
        delivery_id=delivery_method_id,
    )
    db.session.add(order)
    db.session.commit()
    flash("Order successfull!")

    return redirect("/order/success")


@bp.route("/success", methods=["GET"])
@login_required
def success():
    return render_template("order/success.html")
