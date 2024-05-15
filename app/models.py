import datetime
from .database import db
from flask_login import UserMixin


class Size(db.Model):
    __tablename__ = "size"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    size_type_id = db.Column(
        db.Integer, db.ForeignKey("size_type.id", ondelete="CASCADE")
    )
    product_item = db.relationship(
        "ProductItem",
        backref="size",
        cascade="all, delete",
    )


class SizeType(db.Model):
    __tablename__ = "size_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    size = db.relationship(
        "Size",
        backref="size_type",
        cascade="all, delete",
    )


class ProductType(db.Model):
    __tablename__ = "product_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    color = db.Column(db.String(120))
    price = db.Column(db.Float, unique=True)
    img_url = db.Column(db.String(120), unique=True)
    product_item = db.relationship(
        "ProductItem",
        backref="product_type",
        cascade="all, delete",
    )
    product_category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id", ondelete="CASCADE")
    )
class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True)
    subcategory_name = db.Column(db.String(120), unique=True)
    category_name = db.Column(db.String(120))
    product_type = db.relationship(
        "ProductType",
        backref="product_category",
        cascade="all, delete",
    )
    size_type_id = db.Column(
        db.Integer, db.ForeignKey("size_type.id", ondelete="CASCADE")
    )


class ProductItem(db.Model):
    __tablename__ = "product_item"
    id = db.Column(db.Integer, primary_key=True)
    stock_number = db.Column(db.Integer, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    size_id = db.Column(db.Integer, db.ForeignKey("size.id", ondelete="CASCADE"))
    product_type_id = db.Column(
        db.Integer, db.ForeignKey("product_type.id", ondelete="CASCADE")
    )
    cart_item = db.relationship(
        "CartItem",
        backref="product_item",
        cascade="all, delete",
    )
    product_monthly_reports = db.relationship(
        "ProductMonthlyReports", backref="product_item"
    )


class CartItem(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True)
    shopping_cart_id = db.Column(
        db.Integer, db.ForeignKey("cart.id", ondelete="CASCADE")
    )
    quantity = db.Column(db.Integer)
    product_item_id = db.Column(db.Integer, db.ForeignKey("product_item.id", ondelete="CASCADE"))


class ShoppingCart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total = db.Column(db.Float)
    cart_item = db.relationship(
        "CartItem",
        backref="cart",
        cascade="all, delete",
    )
    order = db.relationship("Order", backref="cart")
    auth_user_id = db.Column(
        db.Integer, db.ForeignKey("auth_user.id", ondelete="CASCADE")
    )


class AuthUser(UserMixin, db.Model):
    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    cart = db.relationship(
        "ShoppingCart",
        backref="auth_user",
        cascade="all, delete",
    )


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    order_status_id = db.Column(
        db.Integer, db.ForeignKey("order_status.id", ondelete="SET NULL")
    )
    delivery_method_id = db.Column(
        db.Integer, db.ForeignKey("delivery_method.id", ondelete="SET NULL")
    )
    address_id = db.Column(db.Integer, db.ForeignKey("address.id", ondelete="SET NULL"))
    invoice = db.relationship("Invoice", backref="order")
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id", ondelete="SET NULL"))


class DeliveryMethod(db.Model):
    __tablename__ = "delivery_method"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    price = db.Column(db.Float, unique=True)
    order = db.relationship("Order", backref="delivery_method")


class OrderStatus(db.Model):
    __tablename__ = "order_status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    order = db.relationship("Order", backref="order_status")


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(120))
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    order = db.relationship("Order", backref="address")


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id", ondelete="SET NULL"))


class CityMonthlyReports(db.Model):
    __tablename__ = "city_monthly_reports"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120))
    month = db.Column(db.String(120))
    year = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total = db.Column(db.Float)


class InvoiceMonthlyReports(db.Model):
    __tablename__ = "invoice_monthly_reports"
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(120))
    year = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total = db.Column(db.Float)


class ProductMonthlyReports(db.Model):
    __tablename__ = "product_monthly_reports"
    id = db.Column(db.Integer, primary_key=True)
    product_item_id = db.Column(db.Integer, db.ForeignKey("product_item.id", ondelete="SET NULL"))
    month = db.Column(db.String(120))
    year = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total = db.Column(db.Float)
