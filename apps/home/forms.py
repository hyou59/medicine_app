from flask_wtf import FlaskForm
# ブラウザでフォームデータを扱うためのライブラリ
from wtforms import StringField, SubmitField
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
    submit = SubmitField("更新")


class DeleteMedicineForm(FlaskForm):
    submit = SubmitField("選択したお薬を削除")