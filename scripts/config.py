import os


class Config:
	SECRET_KEY = os.environ['SECRET_KEY']
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLACHEMY_TRACK_MODIFICATIONS']
	
	conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
	conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
	
	DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
		dbuser=db_uri_info['user'],
		dbpass=os.environ['password'],
		dbhost=os.environ['host'],
		dbname=os.environ['dbname']
	)

class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    pass

