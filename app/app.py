from flask import Flask
import logging
from flask_login import LoginManager

from models import load_user, db
from views import bp

app = Flask(__name__)

# データベースとの接続の設定を定義
app.config['SQLALCHEMY_DATABASE_URI'] = \
  'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
  'user': "user",
  'password': "password",
  'host': "db",
  'db_name': "todo_app"
  })

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET'

db.init_app(app)

logging.basicConfig(level=logging.DEBUG) 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user)
login_manager.login_view = "root.login"

# ルーティングの設定
app.register_blueprint(bp)

if __name__ == "__main__":
    with app.app_context():  
        db.create_all()       
    app.run(host="0.0.0.0", debug=True)
