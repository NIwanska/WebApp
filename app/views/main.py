from flask import render_template, Blueprint
from ..models import Product

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/")
def home():
    products = Product.query.all()
    return render_template("main/main.html")
