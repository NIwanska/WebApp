from flask import render_template, Blueprint
from ..models import ProductType, ProductCategory
from flask_login import current_user

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)

@bp.route("/")
@bp.route("/category/<int:category_id>")
def home(category_id=None):
    categories = ProductCategory.query.order_by(ProductCategory.category_name, ProductCategory.subcategory_name).all()
    if category_id:
        products = ProductType.query.filter_by(product_category_id=category_id).all()
    else:
        products = ProductType.query.all()
    return render_template("main/main.html", products=products, categories=categories, current_user=current_user)
