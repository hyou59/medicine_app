# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
from models.models import Medicine, User
from models.database import db_session
from datetime import timedelta, date
from flask import session, redirect, url_for
from hashlib import sha256
from app import key
from app.session_check import session_check

# Flaskオブジェクトの生成
app = Flask(__name__)
# 暗号化キーの定義
app.secret_key = key.SECRET_KEY


# ホーム画面
@app.route("/index")
def index():
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    # テーブル内の対象ユーザのデータを全件取得
    all_medicine = Medicine.query.filter_by(user_name=name)

    # レコードの存在チェック
    if all_medicine is None:
        # レコードが無ければ以降の処理をスキップ
        return render_template("index.html", name=name)

    medi_list = []
    for medicine in all_medicine:
        medi_oin = medicine.medi_oin
        
        # テーブルから取得した情報をリスト内に辞書型で格納
        medi_dict = {}
        medi_dict["id"] = medicine.id
        medi_dict["medi_name"] = medicine.medi_name
        medi_dict["medi_type"] = medicine.medi_type
        medi_dict["updated_at"] = medicine.updated_at
        medi_dict["medi_date"] = medicine.medi_date

        # 薬の残量（日分）
        medi_dict["medi_residue"] = ""

        # 薬が切れる予測日 - 今日の日付 により、薬の残量（日分）を算出
        medi_dict["medi_residue"] = (medi_dict["medi_date"] - date.today()).days

        # 塗り薬の残り本数
        medi_dict["medi_number"] = ""

        # 塗り薬の場合は塗り薬の残り本数を算出する。残り日数を薬の本数で割り、切り上げした値を設定
        if medi_dict["medi_type"] == "塗り薬":
            medi_dict["medi_number"] = -(-int(medi_dict["medi_residue"]) // medi_oin)

            # 計算結果がマイナスであれば0を設定
            if medi_dict["medi_number"] < 0:
                medi_dict["medi_number"] = 0

        # リストに格納
        medi_list.append(medi_dict)

    # 薬が切れる最も直近の予測日を取得
    min_date = Medicine.query.filter_by(user_name=name).order_by(Medicine.medi_date).first()

    # レコードの存在チェック
    if min_date is None:
        min_next_day = None
        # レコードが無ければ以降の処理をスキップ
        return render_template("index.html", name=name, medi_list=medi_list, min_next_day=min_next_day)

    min_next_day = min_date.medi_date

    # 診察予定日が今日の日付以前であれば本日と表示
    if min_next_day <= date.today():
        min_next_day = "本日"

    # html側で表示する画面と渡す変数を設定
    return render_template("index.html", name=name, medi_list=medi_list, min_next_day=min_next_day)


# 削除ボタン押下時
@app.route("/delete", methods=["post"])
def delete():
    # フォームで選択されたレコードのidをリストに格納
    id_list = request.form.getlist("delete")
    for id in id_list:
        # 該当するidのレコードを削除する
        content = Medicine.query.filter_by(id=id).first()
        db_session.delete(content)
    # コミットする
    db_session.commit()
    return redirect(url_for("index"))


# 薬の新規登録画面
@app.route("/medicine_registar")
def medicine_registar():
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    return render_template("medicine_registar.html", name=name)


# 薬の新規登録ボタン押下時
@app.route("/medicine_registar/add", methods=["post"])
def medicine_registar_add():
    # フォームから値を取得
    user_name = session["user_name"]
    medi_name = request.form["mediName"]
    medi_type = request.form["mediType"]

    if medi_type == "飲み薬":
        medi_residue = request.form["mediResidue1"]
        # 飲み薬の１本当たりの使用可能日数は""を設定
        medi_oin = ""
    else:
        # 塗り薬の残量は日数と本数をかけた値を設定
        medi_residue = int(request.form["mediResidue2"]) * int(request.form["mediOin"])
        medi_oin = request.form["mediOin"]
    
    # 診察予定日を算出
    medi_date = date.today() + timedelta(days=int(medi_residue))

    # レコードのインスタンス生成
    content = Medicine(user_name, medi_name, medi_type, medi_oin, date.today(), medi_date)
    # DBに追加してコミット
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))


# お薬更新画面
@app.route("/medicine_update/<int:id>")
def medicine_update(id: int):
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    # 該当するidのレコードを取得する
    record = Medicine.query.filter_by(id=id).first()

    # 別のユーザのidのページの場合、ホーム画面にリダイレクトする
    # 404のページを将来的に表示させる
    if name != record.user_name:
        return redirect(url_for("index", status="not_found"))

    # 薬が切れる予測日-本日 により残量を算出
    medi_residue = (record.medi_date - date.today()).days

    if record.medi_type == "塗り薬":
        # 残りの塗り薬の本数を切り上げで算出
        medi_residue = -(-int(medi_residue) // record.medi_oin)
    
    return render_template("medicine_update.html", name=name, record=record, medi_residue=medi_residue)


@app.route("/medicine_update/<int:id>/post", methods=["post"])
def medicine_update_post(id: int):
    # 対象のidのレコードを選択する
    record = Medicine.query.filter_by(id=id).first()

    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    # 別のユーザのidのページの場合、ホーム画面にリダイレクトする
    # 404のページを将来的に表示させる
    if name != record.user_name:
        return redirect(url_for("index", status="not_found"))

    # フォームから値を取得
    record.medi_name = request.form["mediName"]

    if record.medi_type == "飲み薬":
        medi_residue = request.form["mediResidue1"]
        # 飲み薬であれば1本当たりの使用可能数は""を設定
        record.medi_oin = ""
    else:
        # 塗り薬であれば本数と日数をかけた値を残量に設定
        medi_residue = int(request.form["mediResidue2"]) * int(request.form["mediOin"])
        record.medi_oin = request.form["mediOin"]

    # 更新日に今日の日付を設定
    record.updated_at = date.today()

    # 薬が無くなる予測日を算出
    record.medi_date = date.today() + timedelta(days=int(medi_residue))

    # コミットする
    db_session.commit()
    return redirect(url_for("index"))


# ログイン画面
@app.route("/")
@app.route("/top")
def top():
    # ステータスを取得
    status = request.args.get("status")
    return render_template("top.html", status=status)


# ログイン時の処理
@app.route("/login", methods=["post"])
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
            return redirect(url_for("index"))
        
        else:
            # パスワードが一致しなければ、statusにuser_notfoundを設定しリダイレクト
            return redirect(url_for("top", status="user_notfound"))
    
    else:
        # ユーザとパスワードの組み合わせが無ければ、statusにuser_notfoundを設定しリダイレクト
        return redirect(url_for("top", status="user_notfound"))


# ログアウト時の処理
@app.route("/logout")
def logout():
    # セッション情報からユーザを削除する
    session.pop("user_name", None)
    # トップ画面へ移動
    return redirect(url_for("top", status="logout"))


# アカウント新規登録画面
@app.route("/newcomer")
def newcomer():
    # ステータスを取得
    status = request.args.get("status")
    return render_template("newcomer.html", status=status)


# アカウント新規登録ボタン押下時
@app.route("/registar", methods=["post"])
def registar():
    # ユーザ名をフォームから取得する
    user_name = request.form["user_name"]
    # usersテーブルから対象のレコードを抽出する
    user = User.query.filter_by(user_name=user_name).first()

    # ユーザが既に登録されていれば、アカウント登録画面へリダイレクト
    if user:
        return redirect(url_for("newcomer", status="exist_user"))

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
        return redirect(url_for("index"))


# カレンダー画面
@app.route('/calendar')
def calendar():
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    return render_template('calendar.html', name=name)
    

if __name__ == "__main__":
    app.run(debug=True)