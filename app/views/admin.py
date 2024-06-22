from flask import render_template, Blueprint
from ..models import ProductType, ProductCategory
from flask_login import current_user
from ..utils.admin_utils import products_monthly_reports_hist, cities_monthly_reports_hist
from ..utils.admin_utils import invoices_monthly_reports_hist


bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/admin",
)

@bp.route("/<int:year>/")
def admin_view(year=2024):
    years = [i for i in range(1995, 2024)]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    products_monthly_reports_hist(months)
    cities_monthly_reports_hist(months)
    invoices_monthly_reports_hist(months)
    return render_template("admin/admin.html", years=years, months=months, year=year)

# @bp.route("/<int:year>/")
# def admin_view_year(year):
#     products_monthly_reports_hist()
#     years = [i for i in range(1995, 2024)]
#     months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#     return render_template("admin/admin.html", years=years, months=months, year=year)