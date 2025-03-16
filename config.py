import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///prod.db")
    DEBUG = os.getenv("DEBUG", True)
    SQLALCHEMY_ECHO = os.getenv("ECHO", False)
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    ALLOWED_ORIGIN_1 = os.getenv('ALLOWED_ORIGIN_1')
    ALLOWED_ORIGIN_2 = os.getenv('ALLOWED_ORIGIN_2')
    ALLOWED_ORIGIN_3 = os.getenv('ALLOWED_ORIGIN_3')
    MY_JWT_SECRET_KEY = os.getenv('MY_JWT_SECRET_KEY')
    GEMINI_KEY = os.getenv('GEMINI_KEY')