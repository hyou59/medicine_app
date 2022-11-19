from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from apps.config import config
import logging

# SQLAlchemyをインスタンス化する
db = SQLAlchemy()
# CSRFProtectをインスタンス化する
csrf = CSRFProtect()
# LoginManagerをインスタンス化する
login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを設定する
login_manager.login_view = "auth.login"
# login_view属性にログイン後表示するメッセージを指定する
# ここでは空を設定
login_manager.login_message = ""


# create_app関数を作成する
def create_app(config_key):
    # Flaskインスタンス生成
    app = Flask(__name__)

    # config_keyにマッチする環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])

    # SQLAlchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)
    # CSRFProtectとアプリを連携する
    csrf.init_app(app)
    
    # login_managerをアプリケーションと連携する
    login_manager.init_app(app)

    # ログ出力のレベルの設定
    app.logger.setLevel(logging.DEBUG)
    # リダイレクトを中断しないようにする
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    # DebugToolbarExtensionsアプリケーションをセットする
    toolbar = DebugToolbarExtension(app)

    # authパッケージからviewsをimportする
    from apps.auth import views as auth_views
    # homeパッケージからviewsをimportする
    from apps.home import views as home_views

    # register_blueprintを使いviewsのauthをアプリへ登録する
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    # register_blueprintを使いviewsのhomeをアプリへ登録する
    app.register_blueprint(home_views.hm)
    # カスタムエラー画面を登録する
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app


# 登録したエンドポイント名の関数を作成し、404や500が発生した際に指定したHTMLを返す
def page_not_found(e):
    # 404 Not Found
    return render_template("404.html"), 404

def internal_server_error(e):
    # 500 internal_server_error
    return render_template("500.html"), 500