import datetime
from .database import db


class Size(db.Model):
    __tablename__ = "size"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    size_type_id = db.Column(db.Integer, db.ForeignKey("size_type.id"))


class SizeType(db.Model):
    __tablename__ = "size_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    size = db.relationship("Size", backref="size_type")


class ProductType(db.Model):
    __tablename__ = "product_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    color = db.Column(db.String(120))
    price = db.Column(db.Float, unique=True)
    img_url = db.Column(db.String(120), unique=True)
    product = db.relationship("Product", backref="product_type")


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    stock_number = db.Column(db.Integer, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    size_id = db.Column(db.Integer, db.ForeignKey("size.id"))
    product_type_id = db.Column(db.Integer, db.ForeignKey("product_type.id"))
    cart_item = db.relationship("CartItem", backref="product")


class CartItem(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))


class ShoppingCart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    cart_item = db.relationship("CartItem", backref="cart")
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    auth_user_id = db.Column(db.Integer, db.ForeignKey("auth_user.id"))


class AuthUser(db.Model):
    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    cart = db.relationship("ShoppingCart", backref="auth_user")


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    order_status_id = db.Column(db.Integer, db.ForeignKey("order_status.id"))
    delivery_id = db.Column(db.Integer, db.ForeignKey("delivery.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    auth_user_id = db.Column(db.Integer, db.ForeignKey("auth_user.id"))
    invoice = db.relationship("Invoice", backref="order")


class Delivery(db.Model):
    __tablename__ = "delivery"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    price = db.Column(db.Float, unique=True)
    order = db.relationship("Order", backref="delivery")


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
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))


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
    month = db.Column(db.String(120))
    year = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total = db.Column(db.Float)
