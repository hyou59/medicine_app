from flask import Flask
from apps import key
from flask_debugtoolbar import DebugToolbarExtension
import logging

# create_app関数を作成する
def create_app():
    # Flaskインスタンス生成
    app = Flask(__name__)

    # 暗号化キーの定義
    app.secret_key = key.SECRET_KEY

    # ログレベルの設定
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
    app.register_blueprint(home_views.home, url_prefix="/home")

    return app