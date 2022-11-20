# ベースイメージの指定
FROM python:3.9

# apt-getのversionを更新し、SQLite3のインストール
RUN apt-get update && apt-get install -y sqlite3 && apt-get install -y libsqlite3-dev

# コンテナ上のワーキングディレクトリの指定
WORKDIR /usr/src/

# ディレクトリとファイルのコピー
COPY ./apps /usr/src/apps
COPY ./tests /usr/src/tests
COPY ./local.sqlite /usr/src/local.sqlite
COPY ./requirements.txt /usr/src/requirements.txt

# pipのversionの更新
RUN pip install --upgrade pip

# 必要なライブラリをコンテナ内の環境にインストール
RUN pip install -r requirements.txt

# "building..."を表示させる処理
RUN echo "building..."

# 必要な各環境変数を設定
ENV FLASK_APP "apps.app:create_app('local')"

# 特定のネットワーク・ポートをコンテナが実行時にリッスン
EXPOSE 5000

# "docker run"実行時に実行される処理
CMD ["flask", "run", "-h", "0.0.0.0"]