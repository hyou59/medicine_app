from tests.auth.test_views import signup
from collections import defaultdict


# 飲み薬の登録の実行関数
def internal_register(client, medi_name, mediType, mediResidue1):
    data = dict(medi_name=medi_name, mediType=mediType, mediResidue1=mediResidue1)
    return client.post("/medicine_register", data=data, follow_redirects=True)


# 塗り薬の登録の実行関数
def ointment_register(client, medi_name, mediType, mediResidue2, mediOin):
    data = dict(medi_name=medi_name, mediType=mediType, mediResidue2=mediResidue2, mediOin=mediOin)
    return client.post("/medicine_register", data=data, follow_redirects=True)


# 飲み薬の更新の実行関数
def internal_upload(client, medi_name, mediResidue1):
    data = dict(medi_name=medi_name, mediResidue1=mediResidue1)
    return client.post("/medicine_update/1", data=data, follow_redirects=True)


# 塗り薬の更新の実行関数
def ointment_upload(client, medi_name, mediResidue2, mediOin):
    data = dict(medi_name=medi_name, mediResidue2=mediResidue2, mediOin=mediOin)
    return client.post("/medicine_update/1", data=data, follow_redirects=True)


# 薬の削除の実行関数
def medicine_delete(client, del_list):
    # 辞書の中にリストを格納する
    data = defaultdict(list)
    # deleteのキーに値を格納する
    for i in del_list:
        data["delete"].append(i)
    return client.post("/delete", data=data, follow_redirects=True)


# トップ画面のテスト
def test_index(client):
    rv = client.get("/")
    assert "トップ" in rv.data.decode()


# 飲み薬の登録のテスト
def test_medicine_register1(client):
    # サインアップを実行する
    signup(client, "user1", "password")
    rv = internal_register(client, "薬1", "飲み薬", 30)
    assert "次回の診察" in rv.data.decode()
    assert "薬1" in rv.data.decode()


# 塗り薬の登録のテスト
def test_medicine_register2(client):
    # サインアップを実行する
    signup(client, "user1", "password")
    rv = ointment_register(client, "薬1", "塗り薬", 3, 4)
    assert "次回の診察" in rv.data.decode()
    assert "薬1" in rv.data.decode()


# 飲み薬の更新のテスト
def test_medicine_upload1(client):
    # サインアップを実行する
    signup(client, "user1", "password")
    # 飲み薬を登録する
    internal_register(client, "薬1", "飲み薬", 30)
    # 更新する
    rv = internal_upload(client, "薬2", 0)
    assert "薬2" in rv.data.decode()
    assert "本日" in rv.data.decode()


# 塗り薬の更新のテスト
def test_medicine_upload2(client):
    # サインアップを実行する
    signup(client, "user1", "password")
    # 飲み薬を登録する
    ointment_register(client, "薬1", "塗り薬", 3, 4)
    # 更新する
    rv = ointment_upload(client, "薬2", 0, 10)
    assert "薬2" in rv.data.decode()
    assert "本日" in rv.data.decode()


# 薬の削除のテスト
def test_medicine_delete(client):
    # サインアップを実行する
    signup(client, "user1", "password")
    # 薬を登録する
    internal_register(client, "薬1", "飲み薬", 30)
    ointment_register(client, "薬2", "塗り薬", 3, 4)
    # 薬を削除する
    del_list = [1, 2]
    rv = medicine_delete(client, del_list)
    assert "薬1" not in rv.data.decode()
    assert "薬2" not in rv.data.decode()


# カレンダー画面のテスト
def test_calendar(client):
    # サインアップを実行する
    signup(client, "user1", "password")
    # カレンダー画面を表示する
    rv = client.get("/calendar")
    assert "カレンダー表示画面" in rv.data.decode()
    # assert "月" in rv.data.decode()


# カスタムエラー画面のテスト
def test_custom_error(client):
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()