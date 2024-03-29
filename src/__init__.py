from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration for upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

db = SQLAlchemy(app)
#db.init_app(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"



from src.users.views import users
from src.admin.views import admin
from src.error_pages.views import error_pages
from src.core.views import core
app.register_blueprint(users)
app.register_blueprint(admin)
app.register_blueprint(error_pages)
app.register_blueprint(core)

