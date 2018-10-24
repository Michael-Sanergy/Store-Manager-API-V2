import os


class Config:
    """Common configurations"""
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
