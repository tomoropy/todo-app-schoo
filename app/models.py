from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

# # 認証ユーザーの呼び出し方を定義します
def load_user(user_id):
    return User.query.get(int(user_id))

# Userテーブルの定義
class User(UserMixin, db.Model):
    tablename = 'users'

    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    # Userクラスをインスタンス化した時に各カラムを引数として使えるように設定します
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    # 入力されたパスワードとハッシュ化されたパスワードを比較して検証する
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    # メールアドレスからユーザーを検索する
    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
