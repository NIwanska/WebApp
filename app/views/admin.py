from flask import render_template, Blueprint
from ..models import ProductType, ProductCategory
from flask_login import current_user
from ..utils.admin_utils import products_monthly_reports_hist, cities_monthly_reports_hist
from ..utils.admin_utils import invoices_monthly_reports_hist, products_monthly_reports_pie


bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/admin",
)

@bp.route("/products/<int:year>/")
def admin_view_products(year=2024):
    years = [i for i in range(1995, 2024)]
    months = [str(i) for i in range(1, 13)]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    products_monthly_reports_hist(year, months, months_names)
    products_monthly_reports_pie(year, months, months_names)
    return render_template("admin/admin_products.html", years=years, months=months_names, year=year)

@bp.route("/cities/<int:year>/")
def admin_view_cities(year=2024):
    years = [i for i in range(1995, 2024)]
    months = [str(i) for i in range(1, 13)]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    cities_monthly_reports_hist(year, months, months_names)
    return render_template("admin/admin_cities.html", years=years, months=months_names, year=year)

@bp.route("/invoices/<int:year>/")
def admin_view_invoices(year=2024):
    years = [str(i) for i in range(1995, 2024)]
    months = [str(i) for i in range(1, 13)]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    invoices_monthly_reports_hist(year, months, months_names)
    return render_template("admin/admin_invoices.html", years=years, months=months_names, year=year)



# @bp.route("/<int:year>/")
# def admin_view(year=2024):
#     years = [i for i in range(1995, 2024)]
#     months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#     products_monthly_reports_hist(months)
#     cities_monthly_reports_hist(months)
#     invoices_monthly_reports_hist(months)
#     return render_template("admin/admin.html", years=years, months=months, year=year)

# @bp.route("/<int:year>/")
# def admin_view_year(year):
#     products_monthly_reports_hist()
#     years = [i for i in range(1995, 2024)]
#     months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#     return render_template("admin/admin.html", years=years, months=months, year=year)
