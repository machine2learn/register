import configparser
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT, 'config.ini')

SQLALCHEMY = 'SQLALCHEMY'
MAIL = 'MAIL'
FLASK = 'FLASK'
APP = 'APP'


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class ConfigApp(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)

    def get(self, section, param):
        return self.config.get(section, param)

    def mail_from(self):
        if 'MAIL_USER' in os.environ:
            return os.environ['MAIL_FROM']
        return self.get(MAIL, 'MAIL_FROM')

    def mail_sengrid_api_key(self):
        if 'SENDGRID_API_KEY' in os.environ:
            return os.environ['SENDGRID_API_KEY']
        return self.get(MAIL, 'SENDGRID_API_KEY')

    def database_uri(self):
        # CHECK ENVIROMENT VARIABLES
        if 'DB_HOST' in os.environ and 'DB_NAME' in os.environ and 'DB_USER' in os.environ and 'DB_PASSWORD' in os.environ and 'DB_NAME' in os.environ:
            user = os.environ['DB_USER']
            password = os.environ['DB_PASSWORD']
            name = os.environ['DB_NAME']
            host = os.environ['DB_HOST']
            return f'postgresql+psycopg2://{user}:{password}@{host}/{name}'
        elif 'DB_HOST' in os.environ:
            return os.environ['DB_HOST']

        # CHECK app_config.ini
        if self.get(SQLALCHEMY, 'POSTGRES_DB') not in [None, 'None', 'none']:
            user = self.get(SQLALCHEMY, 'POSTGRES_USER')
            password = self.get(SQLALCHEMY, 'POSTGRES_PW')
            name = self.get(SQLALCHEMY, 'POSTGRES_DB')
            host = self.get(SQLALCHEMY, 'POSTGRES_URL')
            return f'postgresql+psycopg2://{user}:{password}@{host}/{name}'
        return self.get(SQLALCHEMY, 'DB_HOST')

    def debug(self):
        if 'DEBUG' in os.environ:
            return str2bool(os.environ['DEBUG'])
        return str2bool(self.get(FLASK, 'DEBUG'))

    def threaded(self):
        return str2bool(self.get(FLASK, 'THREADED'))

    def host(self):
        return self.get(FLASK, 'HOST')

    def port(self):
        return self.get(FLASK, 'PORT')

    def ezeeai_url(self):
        if 'EZEEAIURL' in os.environ:
            return os.environ['EZEEAIURL']
        return self.get(APP, 'EZEEAIURL')
