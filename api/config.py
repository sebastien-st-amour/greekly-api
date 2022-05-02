import os, json

class Config:

    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    GREEKLY_DB_SECRET = json.loads(os.getenv('GREEKLYAPICLUSTER_SECRET', '{}'))
    DB_USER = GREEKLY_DB_SECRET.get('username')
    DB_PASSWORD = GREEKLY_DB_SECRET.get('password')
    DB_HOST = GREEKLY_DB_SECRET.get('host')
    DB_PORT = GREEKLY_DB_SECRET.get('port')
    DB_NAME = GREEKLY_DB_SECRET.get('dbname')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "this-is-the-default-key")
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class ProductionConfig(Config):

    pass

class StagingConfig(Config):

    pass

class DevelopmentConfig(Config):

    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'