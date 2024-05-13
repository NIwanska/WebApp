from flask import render_template, Blueprint

bp = Blueprint(
    "product",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/product")
def product_list():
    # Do some stuff
    return render_template("product/product.html")
