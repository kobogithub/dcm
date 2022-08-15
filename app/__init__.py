from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carem.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)
#login_manager.login_view = "login_page"
#login_manager.login_message_category = "info"
from app import routes
