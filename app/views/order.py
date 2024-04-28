from flask import render_template, Blueprint, request
from ..models import Product

bp = Blueprint(
    "order",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/order",
)


@bp.route("/")
def index():
    return render_template("order/make_order.html")


@bp.route("/submit_order", methods=["POST"])
def submit_order():
    item = request.form["item"]
    size = request.form["size"]
    quantity = request.form["quantity"]
    name = request.form["name"]
    email = request.form["email"]

    # Process the order, e.g., save to a database, send confirmation email, etc.

    return "Order placed successfully!"
