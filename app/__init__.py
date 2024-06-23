from flask import Flask
from .config import Config, ConfigTest
from .views import main, cart, products, order, auth, orders
from .database import db
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import SizeType, Size, ProductType, ProductCategory, DeliveryMethod, OrderStatus, ProductItem
import csv
import app.db_events  

login_manager = LoginManager()


def create_app(test_mode = False):
    app = Flask(__name__)
    if test_mode is True:
        app.config.from_object(ConfigTest())
    else:
        app.config.from_object(Config())
    migrate = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Db created")
        add_data_to_sqlalchemy()

    login_manager.init_app(app)
    from .models import AuthUser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return AuthUser.query.get(int(user_id))

    app.register_blueprint(main.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(orders.bp)
    app.jinja_env.globals.update(max=max, min=min)

    # create_view_sql = """
    # CREATE VIEW denormalized_cart_items AS
    # SELECT 
    #     ci.id AS cart_item_id,
    #     ci.quantity,
    #     pt.name AS product_name,
    #     pt.price,
    #     pt.img_url,
    #     s.name AS size_name,
    #     ci.shopping_cart_id,
    #     sc.auth_user_id
    # FROM 
    #     cart_item ci
    # JOIN 
    #     product_item pi ON pi.id = ci.product_item_id
    # JOIN 
    #     product_type pt ON pt.id = pi.product_type_id
    # JOIN 
    #     size s ON s.id = pi.size_id
    # JOIN 
    #     shopping_cart sc ON sc.id = ci.shopping_cart_id;
    # """

    # with app.app_context():
    #     with db.engine.connect() as connection:
    #         connection.execute(create_view_sql)
    

    return app


    
def add_data_to_sqlalchemy():

    if not SizeType.query.first():
        

        with open('./csv_db/size_type.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = SizeType(id=int(row[0]), name=row[1])
                    db.session.add(new_row) 

    if not Size.query.first():
        with open('./csv_db/size.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = Size(id=int(row[0]), name=row[1], size_type_id=int(row[2])) 
                    db.session.add(new_row) 

    
    if not ProductCategory.query.first():
        with open('./csv_db/product_category.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = ProductCategory(id=int(row[0]), subcategory_name=row[1], category_name=row[2], size_type_id=int(row[3]))
                    db.session.add(new_row) 

    
    if not DeliveryMethod.query.first():
        with open('./csv_db/delivery_method.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = DeliveryMethod(id=int(row[0]), name=row[1], price=float(row[2]))
                    db.session.add(new_row) 

    
    if not OrderStatus.query.first():
        with open('./csv_db/order_status.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = OrderStatus(id=int(row[0]), name=row[1])
                    db.session.add(new_row) 

    if not ProductType.query.first():
        with open('./csv_db/product_type.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = ProductType(id=int(row[0]), name=row[1], color=row[5], price=float(row[2]), img_url=row[3], product_category_id=int(row[4]))
                    db.session.add(new_row) 

    if not ProductItem.query.first():
        with open('./csv_db/product_item.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    new_row = ProductItem(id=int(row[0]), stock_number=row[1], timestamp=row[2], size_id=int(row[3]), product_type_id=int(row[4]))
                    db.session.add(new_row) 
    db.session.commit()

