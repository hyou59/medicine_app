from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from flask_paginate import Pagination, get_page_parameter
from datetime import timedelta, date, datetime
from apps.home.forms import NewMedicineForm, UpdateMedicineForm, DeleteMedicineForm, MedicineExaminationForm
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.home.models import Medicine
from flask_login import login_required, current_user

# Blueprintでhomeアプリを生成する
hm = Blueprint(
    "home",
    __name__,
    template_folder="templates",
)

# トップ画面
@hm.route("/")
@hm.route("/index")
def index():
    return render_template("home/index.html")


# ホーム画面
@hm.route("/home")
@login_required
def home():
    logger = current_app.logger
    logger.debug("ユーザー名チェック：" + str(current_user))

    delete_form = DeleteMedicineForm()
    min_next_day = None

    # テーブル内の対象ユーザのデータを全件取得
    all_medicine = Medicine.query.filter_by(user_name=str(current_user)).all()

    # レコードの存在チェック
    if all_medicine == []:

        logger.debug("all_medicineチェック：" + str(all_medicine))
        # レコードが無ければ以降の処理をスキップ
        return render_template("home/home.html", min_next_day=min_next_day, delete_form=delete_form)

    medi_list = []
    for medicine in all_medicine:
        medi_oin = medicine.medi_oin
        
        # テーブルから取得した情報をリスト内に辞書型で格納
        medi_dict = {}
        medi_dict["id"] = medicine.id
        medi_dict["medi_name"] = medicine.medi_name
        medi_dict["medi_type"] = medicine.medi_type
        medi_dict["updated_at"] = medicine.updated_at.date()
        medi_dict["medi_date"] = medicine.medi_date

        # 薬が切れる予測日 - 今日の日付 により、薬の残量（日分）を算出
        medi_dict["medi_residue"] = (medi_dict["medi_date"] - date.today()).days

        # 塗り薬の場合は塗り薬の残り本数を算出する。残り日数を薬の本数で割り、切り上げした値を設定
        if medi_dict["medi_type"] == "塗り薬":
            medi_dict["medi_number"] = -(-int(medi_dict["medi_residue"]) // medi_oin)

            # 計算結果がマイナスであれば0を設定
            if medi_dict["medi_number"] < 0:
                medi_dict["medi_number"] = 0

        # リストに格納
        medi_list.append(medi_dict)

    # ページネーションの設定
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = medi_list[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(medi_list), per_page=10, css_framework='bootstrap5')

    # 薬が切れる最も直近の予測日を取得
    min_date = Medicine.query.filter_by(user_name=str(current_user)).order_by(Medicine.medi_date).first()

    min_next_day = min_date.medi_date
    # 診察予定日が今日の日付以前であれば本日と表示
    if min_next_day <= date.today():
        min_next_day = "本日"

    return render_template("home/home.html", min_next_day=min_next_day, delete_form=delete_form, rows=res, pagination=pagination)


# 受診記録画面
@hm.route("/medical_examination", methods=["GET", "POST"])
@login_required
def medical_examination():
    logger = current_app.logger

    # MedicineExaminationFormをインスタンス化する
    form = MedicineExaminationForm()

    # テーブル内の対象ユーザのデータを全件取得
    all_medicine = Medicine.query.filter_by(user_name=str(current_user)).all()

    # レコードの存在チェック
    if all_medicine == []:

        # レコードが無ければ以降の処理をスキップ
        return render_template("home/medical_examination.html", form=form)

    medi_list = []
    for medicine in all_medicine:
        medi_oin = medicine.medi_oin
        
        # テーブルから取得した情報をリスト内に辞書型で格納
        medi_dict = {}
        medi_dict["id"] = medicine.id
        medi_dict["medi_name"] = medicine.medi_name
        medi_dict["medi_type"] = medicine.medi_type
        medi_dict["updated_at"] = medicine.updated_at.date()
        medi_dict["medi_date"] = medicine.medi_date

        # 薬が切れる予測日 - 今日の日付 により、薬の残量（日分）を算出
        medi_dict["medi_residue"] = (medi_dict["medi_date"] - date.today()).days

        # 塗り薬の場合は塗り薬の残り本数を算出する。残り日数を薬の本数で割り、切り上げした値を設定
        if medi_dict["medi_type"] == "塗り薬":
            medi_dict["medi_number"] = -(-int(medi_dict["medi_residue"]) // medi_oin)

            # 計算結果がマイナスであれば0を設定
            if medi_dict["medi_number"] < 0:
                medi_dict["medi_number"] = 0

        # リストに格納
        medi_list.append(medi_dict)

    # 登録ボタン押下時
    if form.validate_on_submit():
        logger.debug("登録ボタン押下")

        # フォームで選択されたレコードのidをリストに格納
        unselected_id_list = request.form.getlist("notSeen")
        mediResidue_list = request.form.getlist("mediResidue")

        # 表示されている薬を順番に回す
        for i in range(len(medi_list)):
            # 処方されていない薬はスキップする
            if str(medi_list[i]["id"]) in unselected_id_list:
                logger.debug(str(medi_list[i]["id"]) + "は選択されています:")
                continue

            # 一致するidのレコードを取得
            record = Medicine.query.filter_by(id=medi_list[i]["id"]).first()

            # 薬が無くなる予測日を算出
            if record.medi_type == "飲み薬":
                record.medi_date = record.medi_date + timedelta(days=int(mediResidue_list[i]))
            else:
                # 塗り薬であれば本数と日数をかけた値を残量に設定
                record.medi_date = record.medi_date + (timedelta(days=int(mediResidue_list[i]) * int(record.medi_oin)))

            # 更新日に今日の日付を設定
            record.updated_at = datetime.today()

            # コミットする
            db.session.commit()

        # ホーム画面にメッセージ表示
        flash('処方記録を行いました。')

        return redirect(url_for("home.home"))

    return render_template("home/medical_examination.html", form=form, medi_list=medi_list)


# 削除ボタン押下時
@hm.route("/delete", methods=["post"])
@login_required
def delete():

    msg_list = []
    # フォームで選択されたレコードのidをリストに格納
    id_list = request.form.getlist("delete")
    for id in id_list:

        content = Medicine.query.filter_by(id=id).first()
        # 該当するidのレコードの薬名をリストに格納する
        msg_list.append(content.medi_name)

        # 該当するidのレコードを削除する
        db.session.delete(content)

    # コミットする
    db.session.commit()

    # ホーム画面にメッセージ表示
    for msg in msg_list:
        flash(str(msg) + 'を削除しました。')

    return redirect(url_for("home.home"))


# 薬の新規登録画面
@hm.route("/medicine_register", methods=["GET", "POST"])
@login_required
def medicine_register():

    # NewMedicineFormをインスタンス化する
    form = NewMedicineForm()

    # 登録ボタン押下時にフォームの値をバリデートする
    if form.validate_on_submit():
        # フォームから値を取得
        user_name = str(current_user)
        medi_name = form.medi_name.data
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
        content = Medicine(
            user_name = user_name,
            medi_name = medi_name,
            medi_type = medi_type,
            medi_oin = medi_oin,
            medi_date = medi_date,
            updated_at = datetime.today(),
        )

        # DBに追加してコミット
        db.session.add(content)
        db.session.commit()

        # ホーム画面にメッセージ表示
        flash(str(medi_name) + 'を登録しました。')

        return redirect(url_for("home.home"))

    return render_template("home/medicine_register.html", form=form)


# 薬の更新画面
@hm.route("/medicine_update/<int:id>", methods=["GET", "POST"])
@login_required
def medicine_update(id: int):

    # 該当するidのレコードを取得する
    record = Medicine.query.filter_by(id=id).first()

    # idが存在しない場合、404画面を表示
    if record is None:
        # 404 Not Found
        return render_template("404.html"), 404

    # 別のユーザのページの場合、404画面を表示
    if str(current_user) != record.user_name:
        # 404 Not Found
        return render_template("404.html"), 404

    # 薬が切れる予測日-本日 により残量を算出
    medi_residue = (record.medi_date - date.today()).days

    if record.medi_type == "塗り薬":
        # 残りの塗り薬の本数を切り上げで算出
        medi_residue = -(-int(medi_residue) // record.medi_oin)

    form = UpdateMedicineForm()

    # 更新ボタン押下時にフォームの値をバリデートする
    if form.validate_on_submit():

        # フォームから値を取得
        record.medi_name = form.medi_name.data

        if record.medi_type == "飲み薬":
            medi_residue = request.form["mediResidue1"]
            # 飲み薬であれば1本当たりの使用可能数は""を設定
            record.medi_oin = ""
        else:
            # 塗り薬であれば本数と日数をかけた値を残量に設定
            medi_residue = int(request.form["mediResidue2"]) * int(request.form["mediOin"])
            record.medi_oin = request.form["mediOin"]

        # 更新日に今日の日付を設定
        record.updated_at = datetime.today()

        # 薬が無くなる予測日を算出
        record.medi_date = date.today() + timedelta(days=int(medi_residue))

        # コミットする
        db.session.commit()

        # ホーム画面にメッセージ表示
        flash(str(record.medi_name) + 'を更新しました。')

        return redirect(url_for("home.home"))
    
    return render_template("home/medicine_update.html", record=record, medi_residue=medi_residue, form=form)


# カレンダー画面
@hm.route('/calendar')
@login_required
def calendar():

    return render_template('home/calendar.html')