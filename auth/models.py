from datetime import datetime

from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# db.ModelとUserMixinを継承したUserクラスを作成する
class User(db.Model, UserMixin):
    # テーブル名を指定する
    __tablename__ = "users"
    # id（int：キー情報）
    id = db.Column(db.Integer, primary_key=True)
    # user_name（String(128)：ユーザ名）
    user_name = db.Column(db.String(128))
    # password_hash（String(128)：ハッシュ関数を実行したパスワード）
    password_hash = db.Column(db.String(128))
    # created_at（Datetime：テーブル作成日時）
    created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at（Datetime：更新日時）
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # パスワードをセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")

    # セッター関数でハッシュ化してパスワードをセットする
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # ユーザー名の重複チェックをする
    def is_duplicate_user(self):
        return User.query.filter_by(user_name=self.user_name).first() is not None

    # ハッシュ化されたパスワードの値をチェックをする
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)