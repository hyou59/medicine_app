# テーブル定義

from sqlalchemy import Column, Integer, String, Date
from models.database import Base
from datetime import date


class Medicine(Base):
    # テーブル（medicines）を定義
    __tablename__ = 'medicines'
    # id（int：キー情報）
    id = Column(Integer, primary_key=True)
    # user_name（String(128)：ユーザ名）
    user_name = Column(String(128))
    # mediName（String(128)：お薬の名前）
    medi_name = Column(String(128))
    # mediType（String(128)：お薬の種類(飲み薬、塗り薬)）
    medi_type = Column(String(128))
    # medi_oin（String：塗り薬の１本当たりの使用可能日数）
    medi_oin = Column(Integer)
    # updated_at（Date：お薬の更新日時）
    updated_at = Column(Date, default=date.today())
    # medidate（Date：お薬の切れる予測日）
    medi_date = Column(Date)

    def __init__(self, user_name=None, medi_name=None, medi_type=None, medi_oin=None, updated_at=None, medi_date=None):
        self.user_name = user_name
        self.medi_name = medi_name
        self.medi_type = medi_type
        self.medi_oin = medi_oin
        self.updated_at = updated_at
        self.medi_date = medi_date

    # 出力の際に表示させる形式を定義
    def __repr__(self):
        return '<Name %r>' % (self.user_name)


# ユーザとパスワードを保存するテーブル
class User(Base):
    # テーブル（users）を定義
    __tablename__ = 'users'
    # user_name（String(128)：ユーザid）
    user_name = Column(String(128), primary_key=True)
    # hashed_password（String(128)：ハッシュ関数を実行したパスワード）
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.user_name)
