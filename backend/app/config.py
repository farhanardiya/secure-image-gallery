from datetime import timedelta

ENCRYPTION_KEY=b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'

class Config(object):
    DEBUG = False

class DebugConfig(Config):
    DEBUG = True

    DB_ENGINE = "postgresql"
    DB_USERNAME = "postgres"
    DB_PASS = "postgres"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "db_project"

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        DB_ENGINE,
        DB_USERNAME,
        DB_PASS,
        DB_HOST,
        DB_PORT,
        DB_NAME
    )

    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    JWT_SECRET_KEY = "Super-Secret-Key"

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(hours=1)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

# class ProductionConfig(Config):
#     pass

config_dict = {
    "Debug": DebugConfig
}
