from ..models import Address, db, ShoppingCart, Order, AuthUser, DeliveryMethod, ProductMonthlyReports
import datetime
import matplotlib.pyplot as plt
import numpy as np


def products_monthly_reports_hist(months):
    db.session.query(ProductMonthlyReports)

    for month in months:
        np.random.seed(1)
        x = 1 + np.random.normal(0, 1.5, 200)
        fig, ax = plt.subplots()
        ax.hist(x, bins=8, linewidth=0.5, edgecolor="white")
        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 56), yticks=np.linspace(0, 56, 9))
        plt.savefig(f"./app/static/figures/products/products_monthly_reports_hist_{month}")


def products_monthly_reports_pie(months):
    db.session.query(ProductMonthlyReports)

    for month in months:
        x = [1, 2, 3, 4]
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
        fig, ax = plt.subplots()
        ax.pie(x, colors=colors, radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 8), yticks=np.arange(1, 8))
        plt.savefig(f"./app/static/figures/products/categories_monthly_reports_pie_{month}")


def cities_monthly_reports_hist(months):
    db.session.query(ProductMonthlyReports)

    for month in months:
        np.random.seed(1)
        x = 3 + np.random.normal(0, 1.5, 200)
        fig, ax = plt.subplots()
        ax.hist(x, bins=8, linewidth=0.5, edgecolor="white")
        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 56), yticks=np.linspace(0, 56, 9))
        plt.savefig(f"./app/static/figures/cities/cities_monthly_reports_hist_{month}")


def invoices_monthly_reports_hist(months):
    db.session.query(ProductMonthlyReports)

    for month in months:
        np.random.seed(1)
        x = 3 + np.random.normal(0, 1.5, 200)
        fig, ax = plt.subplots()
        ax.hist(x, bins=8, linewidth=0.5, edgecolor="white")
        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 56), yticks=np.linspace(0, 56, 9))
        plt.savefig(f"./app/static/figures/invoices/invoices_monthly_reports_hist_{month}")


# def get_saved_address_list(current_user_id: int):
#     return (
#         db.session.query(Address)
#         .join(Order, Address.id == Order.address_id)
#         .join(ShoppingCart, ShoppingCart.id == Order.cart_id)
#         .join(AuthUser, AuthUser.id == ShoppingCart.auth_user_id)
#         .filter((AuthUser.id == current_user_id))
#         .all()
#     )


# def create_new_cart(current_user_id: id):

#     cart = ShoppingCart(auth_user_id=current_user_id, timestamp=datetime.datetime.now())
#     db.session.add(cart)
#     db.session.commit()
#     return cart

# if __name__ == "__main__":
    # products_monthly_reports_hist()
