from datetime import timedelta


class Config(object):
    SQLALCHEMY_DATABASE_URI =   'sqlite:///projectDB.sqlite3'   # For using db in instance folder
    SECRET_KEY = 'sengoku1234'
    SECURITY_PASSWORD_SALT= "jidai100"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # to STOP MESSAGES FROM SQL ALCHEMY
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    JWT_SECRET_KEY = 'sengoku1234'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=2)
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    

class devConfig(Config):
    DEBUG = True