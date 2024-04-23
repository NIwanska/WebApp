import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    DEBUG = True
    SECRET_KEY = "aaaaaaaaasecret"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@postgres_db:5432/app_db"
