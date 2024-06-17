from flask import render_template, Blueprint
from ..models import ProductType, Size, ProductItem, db

bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)




@bp.route("/<int:product_id>")
def product_type(product_id):
    product = ProductType.query.get_or_404(product_id)
    sizes = Size.query.filter(Size.id.in_(
        db.session.query(ProductItem.size_id).filter(
            ProductItem.product_type_id == product_id,
            ProductItem.stock_number > 0
        )
    )).all()
    return render_template("product_type/product_type.html", product=product, sizes=sizes)