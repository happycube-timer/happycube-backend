# -*- coding: utf-8 -*-
import os

os_env = os.environ

class Config(object):
    SECRET_KEY = os_env.get('happycube_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'happycube'
    CACHE_REDIS_URL = 'redis://localhost:6379'


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'  # TODO: Change me
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    # DB_NAME = 'happycubedb'
    # DB_USER = 'postgres'
    # DB_PASS = os_env.get('DB_PASS', 'panceta')
    # DB_HOST = 'localhost'
    # DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:panceta@localhost:5432/happycube_dev_db'
    # DB_NAME = 'dev.db'
    # DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'null'  # set to 'redis' to experience the power


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
