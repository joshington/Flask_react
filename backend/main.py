
from flask import Flask
from flask_restx import Api
#from config import DevConfig
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from recipes import recipe_ns
from auth import auth_ns


def  create_app(config):
    app=Flask(__name__)
    #app.config.from_object(DevConfig)
    app.config.from_object(config)
    #doing this since we are inheriting our configs from the class

    db.init_app(app) #telling sqlalchemy to wor with our current application

    migrate=Migrate(app,db)
    JWTManager(app)#this enables flask_jwt to work with our app

    api= Api(app,doc='/docs')

    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db, 
            "Recipe":Recipe,
            "User":User
        }
    #====instead of running our app from the below code block, we are just going to return our 
    #app
    return app
    #if __name__ == "__main__":
    #    app.run()