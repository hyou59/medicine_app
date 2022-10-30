from flask import Blueprint, render_template, request
from flask import session, redirect, url_for
from hashlib import sha256
from models.models import User
from models.database import db_session
from apps import key

# Blueprintでauthアプリを生成する
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# ログイン画面
@auth.route("/")
@auth.route("/top")
def top():
    # ステータスを取得
    status = request.args.get("status")
    return render_template("auth/top.html", status=status)


# ログイン時の処理
@auth.route("/login", methods=["post"])
def login():
    # フォームからユーザ名を取得
    user_name = request.form["user_name"]
    # usersテーブルから対象のレコードを抽出する
    user = User.query.filter_by(user_name=user_name).first()
    
    if user:
        password = request.form["password"]
        # 対象のユーザがあれば、パスワードにユーザ名とソルトを加えハッシュ化する
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        
        if user.hashed_password == hashed_password:
            # パスワードが一致すれば、セッション情報にユーザ名を追加する
            session["user_name"] = user_name
            return redirect(url_for("home.index"))
        
        else:
            # パスワードが一致しなければ、statusにuser_notfoundを設定しリダイレクト
            return redirect(url_for("auth.top", status="user_notfound"))
    
    else:
        # ユーザとパスワードの組み合わせが無ければ、statusにuser_notfoundを設定しリダイレクト
        return redirect(url_for("auth.top", status="user_notfound"))


# ログアウト時の処理
@auth.route("/logout")
def logout():
    # セッション情報からユーザを削除する
    session.pop("user_name", None)
    # トップ画面へ移動
    return redirect(url_for("auth.top", status="logout"))


# アカウント新規登録画面
@auth.route("/newcomer")
def newcomer():
    # ステータスを取得
    status = request.args.get("status")
    return render_template("auth/newcomer.html", status=status)


# アカウント新規登録ボタン押下時
@auth.route("/registar", methods=["post"])
def registar():
    # ユーザ名をフォームから取得する
    user_name = request.form["user_name"]
    # usersテーブルから対象のレコードを抽出する
    user = User.query.filter_by(user_name=user_name).first()

    # ユーザが既に登録されていれば、アカウント登録画面へリダイレクト
    if user:
        return redirect(url_for("auth.newcomer", status="exist_user"))

    # ユーザが重複していなければ、アカウントを登録しログイン
    else:
        # パスワードをフォームから取得する
        password = request.form["password"]
        # パスワードにユーザ名とソルトを加えハッシュ化する
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        # usersテーブルにレコードを追加する
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()

        # セッション情報にユーザ名を追加する
        session["user_name"] = user_name
        return redirect(url_for("home.index"))