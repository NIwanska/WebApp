from flask import render_template, Blueprint
from ..models import ProductType

bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)



# @bp.route('/product/<int:product_id>')
# def product_item(product_id):
#     # Logika do pobrania szczegółów produktu na podstawie product_id
#     return render_template('product_item/product_item.html', product_id=product_id)



@bp.route("/<int:product_id>")
def product_item(product_id):
    product = ProductType.query.get_or_404(product_id)
    return render_template("product_item/product_item.html", product=product)