from flask import Flask
from .config import Config
from .views import main, cart, products, order, auth
from .database import db
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import SizeType, Size, ProductType, ProductCategory, DeliveryMethod, OrderStatus
import csv



login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
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
                    SizeType(id=int(row[0]), name=row[1]) 
                    print(SizeType.query.first())
        # db.session.commit()

    if not Size.query.first():
        with open('./csv_db/size.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    Size(id=int(row[0]), name=row[1], size_type_id=int(row[2])) 

    if not ProductType.query.first():
        with open('./csv_db/product_type.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    ProductType(id=int(row[0]), name=row[1], color=row[5], price=float(row[2]), img_url=row[3], product_category_id=int(row[4]))
    
    if not ProductCategory.query.first():
        with open('./csv_db/product_category.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    ProductCategory(id=int(row[0]), subcategory_name=row[1], category_name=row[2], size_type_id=int(row[3]))
    
    if not DeliveryMethod.query.first():
        with open('./csv_db/delivery_method.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    DeliveryMethod(id=int(row[0]), name=row[1], price=float(row[2]))
    
    if not OrderStatus.query.first():
        with open('./csv_db/order_status.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in data:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    OrderStatus(id=int(row[0]), name=row[1])
    db.session.commit()

