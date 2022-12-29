# Name

お薬管理アプリ

処方しているお薬を記録し、残量の可視化が行えるサービスです。

サービスURL：https://medicine-app.onrender.com/index

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