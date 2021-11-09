import os, json

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    GREEKLY_DB_SECRET = json.loads(os.getenv('GREEKLYAPICLUSTER_SECRET'))
    DB_USER = GREEKLY_DB_SECRET['username']
    DB_PASSWORD = GREEKLY_DB_SECRET['password']
    DB_HOST = GREEKLY_DB_SECRET['host']
    DB_PORT = GREEKLY_DB_SECRET['port']
    DB_NAME = GREEKLY_DB_SECRET['dbname']
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True