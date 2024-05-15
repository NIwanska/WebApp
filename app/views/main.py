from flask import render_template, Blueprint
from ..models import ProductItem
from flask_login import current_user

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/")
def home():
    products = ProductItem.query.all()
    return render_template("main/main.html", current_user=current_user)
