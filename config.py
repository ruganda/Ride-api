import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv("SECRET")
    # DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_URL = 'postgresql://postgres:15december@localhost:5432/ride_db'


class DevelopmentConfiguration(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfiguration(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'postgresql://postgres:15december@localhost:5432/test_db'


class ProductionConfiguration(Config):
    """Configurations for Production."""
    DEBUG = False
    DATABASE_URL = 'postgres://akcolxjufhesko:d01b99b7009c67760234fb1bcb4229e5566490f2e125fc4b539e5d83ee14fbae@ec2-23-21-216-174.compute-1.amazonaws.com:5432/d6bbirccjc7b3e'

app_config = {
    'DEFAULT': DevelopmentConfiguration,
    'TESTING': TestingConfiguration,
    'DEVELOPMENT': DevelopmentConfiguration,
    'PRODUCTION': ProductionConfiguration
}
