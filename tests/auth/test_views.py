# サインアップ関数
def signup(client, user_name, password):
    # サインアップする
    data = dict(user_name=user_name, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)

# ログイン関数
def login(client, user_name, password):
    data = dict(user_name=user_name, password=password)
    return client.post("/login", data=data, follow_redirects=True)

# ログアウト関数
def logout(client):
    return client.post("/logout", follow_redirects=True)


# サインアップ成功とログアウトのテスト
def test_signup(client):
    # サインアップを実行する
    rv = signup(client, "user1", "password")
    assert "user1" in rv.data.decode()
    assert "ログアウト" in rv.data.decode()

    # ログアウトする
    logout(client)
    assert "トップ" in rv.data.decode()


# ログイン成功のテスト
def test_login1(client):
    # サインアップを実行する
    signup(client, "user1", "password")

    # ログアウトする
    logout(client)

    # ログインする
    login(client, "user1", "password")
    rv = client.get("/home")
    assert "user1" in rv.data.decode()


# ログイン失敗のテスト
def test_login2(client):
    # サインアップを実行する
    signup(client, "user1", "password")

    # ログアウトする
    logout(client)

    # ログインする
    login(client, "user2", "password")
    rv = client.get("/home")
    assert "トップ" in rv.data.decode()