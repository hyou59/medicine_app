from datetime import datetime
from apps.app import db

# ユーザーの服用している薬を格納
class Medicine(db.Model):
    # テーブル名を指定する
    __tablename__ = "medicines"

    # id（int：キー情報）
    id = db.Column(db.Integer, primary_key=True)
    # user_name（String(128)：ユーザ名、usersテーブルのuser_nameを外部キーとして設定）
    user_name = db.Column(db.String(128), db.ForeignKey("users.user_name"))
    # medi_name（String(128)：お薬の名前）
    medi_name = db.Column(db.String(128))
    # medi_type（String(128)：お薬の種類(飲み薬、塗り薬)）
    medi_type = db.Column(db.String(128))
    # medi_oin（String：塗り薬の１本当たりの使用可能日数）
    medi_oin = db.Column(db.Integer)
    # medi_date（Date：お薬の切れる予測日）
    medi_date = db.Column(db.Date)
    # created_at（Datetime：テーブル作成日時）
    created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at（Datetime：更新日時）
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


# ユーザーの処方した日時を格納
class Examination(db.Model):
    # テーブル名を指定する
    __tablename__ = "examination"

    # id（int：キー情報）
    id = db.Column(db.Integer, primary_key=True)
    # user_name（String(128)：ユーザ名、usersテーブルのuser_nameを外部キーとして設定）
    user_name = db.Column(db.String(128), db.ForeignKey("users.user_name"))
    # examination_date（Date：受診日）
    examination_date = db.Column(db.Date)
    # created_at（Datetime：テーブル作成日時）
    created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at（Datetime：更新日時）
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # 親レコード削除時に子レコードを削除
    prescription = db.relationship("Prescription", backref="examination", cascade="delete")


# 処方した薬を１つずつ格納
class Prescription(db.Model):
    # テーブル名を指定する
    __tablename__ = "prescription"

    # id（int：キー情報）
    id = db.Column(db.Integer, primary_key=True)
    # prescription_key （Integer：処方キー、examinationテーブルのidを外部キーとして設定）
    prescription_key = db.Column(db.Integer, db.ForeignKey("examination.id"))
    # medi_name（String(128)：お薬の名前）
    medi_name = db.Column(db.String(128))
    # medi_type（String(128)：お薬の種類(飲み薬、塗り薬)）
    medi_type = db.Column(db.String(128))
    # medi_residue（Integer：処方した薬の日数）
    medi_residue = db.Column(db.Integer)
    # created_at（Datetime：テーブル作成日時）
    created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at（Datetime：更新日時）
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())