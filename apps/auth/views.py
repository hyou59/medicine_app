from flask import Blueprint, render_template, flash, redirect, url_for
from apps.auth.forms import LoginForm, NewUserForm
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.auth.models import User
from flask_login import login_user, logout_user, login_required

# Blueprintでauthアプリを生成する
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# ログイン画面
@auth.route("/")
@auth.route("/login", methods=["GET", "POST"])
def login():

    # LoginFormをインスタンス化する
    form = LoginForm()

    if form.validate_on_submit():
        # 一致するユーザーを取得する
        user = User.query.filter_by(user_name=form.user_name.data).first()

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("home.home"))

        # ログイン失敗時のメッセージを表示
        flash("ユーザー名またはパスワードが異なります。")
    
    return render_template("auth/login.html", form=form)


# アカウント新規登録画面
@auth.route("/signup", methods=["GET", "POST"])
def signup():

    # NewUserFormをインスタンス化する
    form = NewUserForm()

    # ボタン押下時にフォームの値をバリデートする
    if form.validate_on_submit():
        # ユーザーを作成する
        user = User(
            user_name=form.user_name.data,
            password=form.password.data,
        )

        # ユーザー名の重複チェックをする
        if user.is_duplicate_user():
            # ユーザー名が既に登録されていればリダイレクトする
            flash("指定のユーザーは登録済です。")
            return redirect(url_for("auth.signup"))

        # ユーザーを追加してコミットする
        db.session.add(user)
        db.session.commit()

        # ユーザー情報をセッションに格納する
        login_user(user)

        # ホーム画面へリダイレクトする
        return redirect(url_for("home.home", form=form))

    return render_template("auth/signup.html", form=form)


# ログアウト時の処理
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    # ログイン画面へ移動
    return redirect(url_for("auth.login"))