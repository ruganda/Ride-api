
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = "secret"

class DevelopmentConfiguration(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfiguration(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True

class ProductionConfiguration(Config):
    """Configurations for Production."""
    DEBUG = False

app_config = {
    'DEFAULT': DevelopmentConfiguration,
    'TESTING': TestingConfiguration,
    'DEVELOPMENT': DevelopmentConfiguration,
    'PRODUCTION': ProductionConfiguration
}