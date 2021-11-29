# FastAPI 入門

Fast API 入門してみた。

---

- [FastAPI 入門](#fastapi-入門)
  - [概要](#概要)
    - [**FastAPI**の特徴](#fastapiの特徴)
  - [環境構築](#環境構築)
    - [**Poetry**とは](#poetryとは)
    - [**Uvicorn**とは](#uvicornとは)
    - [Poetry 定義ファイル作成](#poetry-定義ファイル作成)
    - [apiディレクトリ配下に、__init__.pyとmain.pyを定義する](#apiディレクトリ配下にinitpyとmainpyを定義する)

---

## 概要

### **FastAPI**の特徴

- リクエストとレスポンスのスキーマ定義に合わせて自動的にSwagger UIのドキュメントが生成される
- 上記のスキーマを明示的に定義することにより、型安全な開発が可能
- ASGI（非同期サーバーゲートウェイインターフェース）に対応しているので、非同期処理を行うことができ、高速

スキーマを明示的に定義することによって、\
フロントエンドエンジニアが実装の際に利用するドキュメントを簡単に自動生成でき、\
さらに実際にリクエストパラメータを変更してAPIの呼び出しを試すこともできる。

→**スキーマ駆動開発**を自然的に始めることができる。

## 環境構築

Docker環境を用意。\
詳細は、Dockerfileとdocker-compose.ymlを参照。

### **Poetry**とは

- Pythonのパッケージマネージャの一つ。JavaにおけるMavenのように、パッケージ同士の依存関係を解決する。
  >  poetry では pip が行わないパッケージ同士の依存関係の解決や、lockファイルを利用したバージョン固定、\
  Pythonの仮想環境管理など、より高機能でモダンなバージョン管理が行えます。

**pyproject.toml**は、poetry において依存関係を管理するファイル。

### **Uvicorn**とは

> Uvicorn は uvloop と httptools を使った高速な ASGI サーバの実装です。\
> 最近までPythonには、asyncioフレームワークのための最小限の低レベルサーバー/アプリケーションインターフェースがありませんでした。ASGI仕様はこのギャップを埋めるもので、すべてのasyncioフレームワークで使える共通のツールセットを構築することができるようになりました。\
>ASGIは、PythonのWebフレームワークのエコシステムを実現し、IO負荷の高いコンテキストで高いスループットを達成するという点で、NodeやGoに対して高い競争力を持つようになるはずです。また、WSGIでは扱えないHTTP/2やWebSocketへの対応も行っています。\
> Uvicornは現在、HTTP/1.1とWebSocketをサポートしています。HTTP/2への対応も予定されています。

### Poetry 定義ファイル作成

docker-compose buildでイメージ作成後、下記コマンドでpoetryの初期化、fastapiのインストールを行う。\
引数として、 fastapi と、ASGIサーバーである uvicorn をインストールする依存パッケージとして指定

```sh
# poetry 定義ファイル作成
docker-compose run \
  --entrypoint "poetry init \
    --name demo-app \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  demo-app

# Fast API インストール
docker-compose run --entrypoint "poetry install" demo-app
```

### apiディレクトリ配下に、__init__.pyとmain.pyを定義する

docker-compose upでコンテナ立ち上げ後、<http://localhost:8000/docs>にアクセスすると、\
Swagger UIが確認できる。実際にブラウザ上で定義したAPIを叩くことができる。
