from flask import render_template, Blueprint, request, flash, redirect
from ..models import Address, db, ShoppingCart, Order
from flask_login import login_required, current_user

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
    saved_address_list = Address.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "order/make_order.html", saved_address_list=saved_address_list
    )


@bp.route("/add_address", methods=["GET"])
@login_required
def add_address_get():
    return render_template("order/add_address.html")


@bp.route("/add_address", methods=["POST"])
@login_required
def add_address():
    street = request.form["street"]
    city = request.form["city"]
    country = request.form["country"]
    zip_code = request.form["name"]

    address = Address(
        street=street,
        city=city,
        country=country,
        zip_code=zip_code,
        user_id=current_user.id,
    )

    db.session.add(address)
    db.session.commit()
    flash("Address added successfully!")
    return redirect("/order")


@bp.route("/submit_order", methods=["POST"])
@login_required
def submit_order():
    address_id = request.form["address_id"]
    cart = current_user.cart
    delivery_method_id = request.form["delivery_method_id"]
    order_status_id = 1
    datetime = datetime.datetime.utcnow()
    total = ShoppingCart.total

    order = Order(
        address_id=address_id,
        cart_id=cart.id,
        total=total,
        datetime=datetime,
        order_status_id=order_status_id,
        delivery_id=delivery_method_id,
    )
    db.sesion.add(order)
    db.session.commit()

    return redirect("/order/success")


@bp.route("/success", methods=["GET"])
@login_required
def success():
    return render_template("order/success.html")
