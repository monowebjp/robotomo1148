# Dockerfile
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# requirements.txtをbackendディレクトリからコピー
COPY ../backend/requirements.txt requirements.txt

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをbackendディレクトリからコンテナにコピー
COPY ../backend .

# コンテナを起動したときに実行するコマンド
CMD ["python", "app.py"]