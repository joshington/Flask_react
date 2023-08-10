from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    #decouple reads it and then casts it to a boolean


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR,'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO=True  #generates the sql commands

class ProdConfig(Config):
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR,'test.db')
    SQLALCHEMY_ECHO = False # we dont want any SQL echos to be generated on the cmdline
    TESTING=True #we shall use this for error catching
