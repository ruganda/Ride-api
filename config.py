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
    DATABASE_URL = 'postgresql://postgres:15december@localhost:5432/ride_db'

app_config = {
    'DEFAULT': DevelopmentConfiguration,
    'TESTING': TestingConfiguration,
    'DEVELOPMENT': DevelopmentConfiguration,
    'PRODUCTION': ProductionConfiguration
}
