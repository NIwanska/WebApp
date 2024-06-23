from ..models import Address, db, ProductMonthlyReports, ProductType, ProductItem, ProductCategory, CityMonthlyReports
import datetime
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import func
from matplotlib.ticker import MaxNLocator


def products_monthly_reports_hist(year, months, months_names):
    # for month in months:
    for month_id in range(len(months)):
        month = months[month_id]
        month_name = months_names[month_id]
        top_products = db.session.query(
            ProductItem.id,
            func.sum(ProductMonthlyReports.count).label('total_count')
        ).join(ProductItem, ProductMonthlyReports.product_item_id == ProductItem.id
        ).filter(
            ProductMonthlyReports.year == year,
            ProductMonthlyReports.month == month
        ).group_by(
            ProductItem.id
        ).order_by(
            func.sum(ProductMonthlyReports.count).desc()
        ).limit(10).all()

        product_ids = [product[0] for product in top_products]
        total_counts = [product[1] for product in top_products]

        plt.figure(figsize=(10, 6))
        plt.bar(product_ids, total_counts)
        plt.xlabel('Product ID')
        plt.ylabel('Total Purchases')
        plt.tight_layout()
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig(f"./app/static/figures/products/products_monthly_reports_hist_{month_name}.png")


def products_monthly_reports_pie(year, months, months_names):
    for month_id in range(len(months)):
        month = months[month_id]
        month_name = months_names[month_id]
        category_sales = (
            db.session.query(ProductCategory.category_name, func.sum(ProductMonthlyReports.count).label('total_count'))
            .join(ProductItem, ProductItem.id == ProductMonthlyReports.product_item_id)
            .join(ProductType, ProductType.id == ProductItem.product_type_id)
            .join(ProductCategory, ProductCategory.id == ProductType.product_category_id)
            .filter(ProductMonthlyReports.month == str(month), ProductMonthlyReports.year == year)
            .group_by(ProductCategory.category_name)
            .all()
        )

        labels = [category[0] for category in category_sales]
        sizes = [category[1] for category in category_sales]

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # plt.title(f'Procentowy udział kategorii w zakupach w miesiącu {month} roku {year}')
        plt.savefig(f"./app/static/figures/products/categories_monthly_reports_pie_{month_name}.png")
        plt.close()


def cities_monthly_reports_hist(year, months, months_names):
    # for month in months:
    for month_id in range(len(months)):
        month = months[month_id]
        month_name = months_names[month_id]

        data = db.session.query(
            CityMonthlyReports.city,
            func.sum(CityMonthlyReports.count).label('total_count')
        ).filter(
            CityMonthlyReports.year == year,
            CityMonthlyReports.month == month
        ).group_by(
            CityMonthlyReports.city
        ).limit(10).all()

        cities = [record.city for record in data]
        counts = [record.total_count for record in data]

        plt.figure(figsize=(10, 6))
        plt.bar(cities, counts)
        plt.xlabel('City')
        plt.ylabel('Number of Orders')
        # plt.title(f'Number of Orders per City in {month} {year}')
        plt.xticks(rotation=15, ha='right')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig(f"./app/static/figures/cities/cities_monthly_reports_hist_{month_name}")


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

