from flask_wtf import FlaskForm
# ブラウザでフォームデータを扱うためのライブラリ
from wtforms import StringField, BooleanField, SubmitField
# 必須チェック、文字列の長さチェック用
from wtforms.validators import DataRequired, Length

# お薬の新規作成フォームクラス
class NewMedicineForm(FlaskForm):
    # お薬の名前フォームのmedi_name属性のラベルとバリデータを設定する
    medi_name = StringField(
        "お薬の名前",
        validators=[
            DataRequired(message="お薬の名前は必須です。"),
            Length(max=20, message="お薬の名前は20文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("登録")


# お薬の更新フォームクラス
class UpdateMedicineForm(FlaskForm):
    # お薬の名前フォームのmedi_name属性のラベルとバリデータを設定する
    medi_name = StringField(
        "お薬の名前",
        validators=[
            DataRequired(message="お薬の名前は必須です。"),
            Length(max=20, message="お薬の名前は20文字以内で入力してください。"),
        ],
    )

    # ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("修正")


# お薬の削除フォームクラス
class DeleteMedicineForm(FlaskForm):
    submit = SubmitField("削除")


# 処方記録フォームクラス
class MedicineExaminationForm(FlaskForm):
    submit = SubmitField("登録")


# カレンダーイベント削除フォームクラス
class DeleteCalendarEvent(FlaskForm):
    submit = SubmitField("削除")