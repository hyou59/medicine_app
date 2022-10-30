# セッション確認用の関数を定義

from flask import session, redirect, url_for

def session_check():
    # セッション情報チェック
    if not "user_name" in session:
        # セッション情報にユーザが無ければ、ログイン画面にリダイレクトする
        return redirect(url_for("auth/top", status="logout"))

    # セッション情報からユーザ名を取得する
    name = session["user_name"]

    return name