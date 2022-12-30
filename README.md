# Name

お薬管理アプリ

処方しているお薬を登録し、残量を可視化及びお薬の切れる日付を予測します。
処方の記録も行うことができます。

サービスURL：https://medicine-app.onrender.com/index
<<<<<<< HEAD
=======

# function

ログイン、ログアウト
お薬登録、更新、削除
処方記録の登録、削除
カレンダー表示
レスポンシブデザイン
>>>>>>> develop

# Requirement

python 3.9.0

# Installation
## パッケージインストール
```
pip install -r requirements.txt
```
## DBマイグレート
```
flask db init
flask db migrate
flask db upgrade
```

## アプリケーション起動
```
flask run
```

## テスト実行
```
pytest tests/auth
pytest tests/home
```