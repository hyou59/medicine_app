from datetime import datetime
from apps.app import db

class Medicine(db.Model):
    # テーブル名を指定する
    __tablename__ = "medicines"

    # id（int：キー情報）
    id = db.Column(db.Integer, primary_key=True)
    # user_name（String(128)：ユーザ名、usersテーブルのuser_nameを外部キーとして設定）
    user_name = db.Column(db.String(128), db.ForeignKey("users.user_name"))
    # mediName（String(128)：お薬の名前）
    medi_name = db.Column(db.String(128))
    # mediType（String(128)：お薬の種類(飲み薬、塗り薬)）
    medi_type = db.Column(db.String(128))
    # medi_oin（String：塗り薬の１本当たりの使用可能日数）
    medi_oin = db.Column(db.Integer)
    # medidate（Date：お薬の切れる予測日）
    medi_date = db.Column(db.Date)
    # created_at（Datetime：テーブル作成日時）
    created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at（Datetime：更新日時）
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())