from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from os import path


database = SQLAlchemy()
DB_NAME = "databaseproject.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'random'
    db_path = os.path.join(os.path.dirname(__file__), 'databaseproject.db')
    db_uri = "sqlite:///{}".format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    database.init_app(app)
    migrate = Migrate(app,database)
    
  
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import Student, Teacher, Course, Admin, Department
    create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))
   
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            database.create_all()
            print('Created database. ')
 