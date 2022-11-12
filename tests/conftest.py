import pytest

from apps.app import create_app, db

from apps.auth.models import User
from apps.home.models import Medicine

# フィクスチャ関数を作成する
@pytest.fixture
def fixture_app():
    # セットアップ処理
    # テスト用のコンフィグを使うために引数にtestingを指定する
    app = create_app("testing")

    # データベースを利用するための宣言をする
    app.app_context().push()

    # テスト用のデータベースのテーブルを作成する
    with app.app_context():
        db.create_all()

    # テストを実行する
    yield app

    # クリーンナップ処理
    # usersテーブルのレコードを削除する
    User.query.delete()

    # medicinesテーブルのレコードを削除する
    Medicine.query.delete()

    db.session.commit()

# Flaskのテストクライアントを返すフィクスチャ関数を作成する
@pytest.fixture
def client(fixture_app):
    # Flaskのテスト用クライアントを返す
    return fixture_app.test_client()
