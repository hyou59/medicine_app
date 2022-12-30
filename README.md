# Name

お薬管理アプリ

服用しているお薬を登録し、残量を可視化及びお薬が切れる日付を予測します。  
また処方記録ができ、カレンダー画面から処方記録の閲覧及び削除が行えます。

サービスURL：https://medicine-app.onrender.com/index

# function

ログイン、ログアウト  
お薬登録、更新、削除  
処方記録の登録、削除  
カレンダー表示  

# technology

## フロントエンド
```
Bootstrap5  
HTML5  
CSS3  
JavaScript  
JQuery
```

## バックエンド
```
Python  
Flask
```

## データベース
```
sqlite3
```

## インフラ
```
Docker  
Render
```

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