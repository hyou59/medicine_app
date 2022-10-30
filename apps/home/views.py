from flask import Blueprint, Flask, render_template, request, current_app
from models.models import Medicine, User
from models.database import db_session
from datetime import timedelta, date
from flask import session, redirect, url_for
from hashlib import sha256
from apps.session_check import session_check

# Blueprintでhomeアプリを生成する
home = Blueprint(
    "home",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# ホーム画面
@home.route("/index")
def index():
    logger = current_app.logger
    # ログに出力
    logger.debug("/index")

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
        return render_template("home/index.html", name=name, medi_list=medi_list, min_next_day=min_next_day)

    min_next_day = min_date.medi_date
    # 診察予定日が今日の日付以前であれば本日と表示
    if min_next_day <= date.today():
        min_next_day = "本日"

    # html側で表示する画面と渡す変数を設定
    return render_template("home/index.html", name=name, medi_list=medi_list, min_next_day=min_next_day)


# 削除ボタン押下時
@home.route("/delete", methods=["post"])
def delete():
    # フォームで選択されたレコードのidをリストに格納
    id_list = request.form.getlist("delete")
    for id in id_list:
        # 該当するidのレコードを削除する
        content = Medicine.query.filter_by(id=id).first()
        db_session.delete(content)
    # コミットする
    db_session.commit()
    return redirect(url_for("home.index"))


# 薬の新規登録画面
@home.route("/medicine_registar")
def medicine_registar():
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    return render_template("home/medicine_registar.html", name=name)


# 薬の新規登録ボタン押下時
@home.route("/medicine_registar/add", methods=["post"])
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
    return redirect(url_for("home.index"))


# お薬更新画面
@home.route("/medicine_update/<int:id>")
def medicine_update(id: int):
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    # 該当するidのレコードを取得する
    record = Medicine.query.filter_by(id=id).first()

    # 別のユーザのidのページの場合、ホーム画面にリダイレクトする
    # 404のページを将来的に表示させる
    if name != record.user_name:
        return redirect(url_for("home.index", status="not_found"))

    # 薬が切れる予測日-本日 により残量を算出
    medi_residue = (record.medi_date - date.today()).days

    if record.medi_type == "塗り薬":
        # 残りの塗り薬の本数を切り上げで算出
        medi_residue = -(-int(medi_residue) // record.medi_oin)
    
    return render_template("home/medicine_update.html", name=name, record=record, medi_residue=medi_residue)


# 薬の更新ボタン押下時
@home.route("/medicine_update/<int:id>/post", methods=["post"])
def medicine_update_post(id: int):
    # 対象のidのレコードを選択する
    record = Medicine.query.filter_by(id=id).first()

    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    # 別のユーザのidのページの場合、ホーム画面にリダイレクトする
    # 404のページを将来的に表示させる
    if name != record.user_name:
        return redirect(url_for("home.index", status="not_found"))

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
    return redirect(url_for("home.index"))


# カレンダー画面
@home.route('/calendar')
def calendar():
    # セッション情報をチェックしユーザ名を取得
    name = session_check()

    return render_template('home/calendar.html', name=name)