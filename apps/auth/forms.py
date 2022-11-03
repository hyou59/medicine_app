from flask_wtf import FlaskForm
# ブラウザでフォームデータを扱うためのライブラリ
from wtforms import PasswordField, StringField, SubmitField
# 必須チェック、文字列の長さチェック用
from wtforms.validators import DataRequired, Length

# ログインフォームクラス
class LoginForm(FlaskForm):
    # ユーザーフォームのuser_name属性のラベルとバリデータを設定する
    user_name = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です。"),
            Length(min=4, max=15),
        ],
    )

    # ユーザーフォームのpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
            Length(min=4, max=15),
        ],
    )

    # ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("ログイン")


# ユーザー新規作成フォームクラス
class NewUserForm(FlaskForm):
    user_name = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です。"),
            Length(min=4, max=15, message="ユーザー名は4文字以上で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
            Length(min=4, max=15, message="パスワードは4文字以上で入力してください。"),
        ],
    )

    # ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")