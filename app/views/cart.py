from flask import render_template, Blueprint

bp = Blueprint(
    "cart",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/cart")
def cart_detail():
    # Do some stuff
    return render_template("main/main.html")
