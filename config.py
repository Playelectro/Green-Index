import os

class Config:
	SECRET_KEY = os.environ['SECRET_KEY']
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLACHEMY_TRACK_MODIFICATIONS']

class DevConfig(Config):
    DEBUG = True
	SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass
