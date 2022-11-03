from pathlib import Path
import os

basedir = Path(__file__).parent.parent

# BaseConfigクラスを作成する
class BaseConfig:
    # 暗号化キー
    # SECRET_KEY = "q8wkfsf3re6m2unhyt7n",
    SECRET_KEY = os.urandom(24),
    # CSRF対策に用いる暗号化キー
    WTF_CSRF_SECRET_KEY = os.urandom(24),
    # WTF_CSRF_SECRET_KEY = "AHhejolf74kdivubDdGLG",

# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    # SQliteのデータベースを出力するパスを設定
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    # 警告が出るためFalseを設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    # SQLをコンソールログに出力する設定
    SQLALCHEMY_ECHO = True,

# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    # SQliteのデータベースを出力するパスを設定
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    # 警告が出るためFalseを設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    # CSRFを無効化
    WTF_CSRF_ENABLED = False,

# config辞書にマッピングする
config = {
    "local" : LocalConfig,
    "testing" : TestingConfig,
}