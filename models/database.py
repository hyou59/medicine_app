# DB接続情報

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative  import declarative_base
import os


# database.pyと同じパスにmedicine_app.dbというファイルを絶対パスで定義
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'medicine_app.db')
# SQLiteを利用して1.で定義した絶対パスにDBを構築
engine = create_engine('sqlite:///' + database_file, convert_unicode=True)
# DB接続用インスタンスを生成
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Baseオブジェクトを生成
Base = declarative_base()
# DBの情報をBaseオブジェクトに流し込む
Base.query = db_session.query_property()


def init_db():
    # 対象のテーブルを定義しているファイルを選択
    import models.models
    # テーブルを作成
    Base.metadata.create_all(bind=engine)