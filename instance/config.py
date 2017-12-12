"""
Configuration settings for different app environments
"""
import os


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Thi-is-a-secret-key-pliz-change-it"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgresql@localhost:5432/flask_api'


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgresql@localhost/test_db'


class DevelopmentEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    


class ProductionEnvironment(MainConfiguration):
    DEBUG = False
    TESTING = False


# Dictionary of different configuration environments
application_config = {
    'MainConfig': MainConfiguration,
    'TestingEnv': TestingEnvironment,
    'DevelopmentEnv': DevelopmentEnvironment,
    'ProductionEnv': ProductionEnvironment
}