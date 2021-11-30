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
    - [api ディレクトリ配下に、**init**.py と main.py を定義する](#api-ディレクトリ配下にinitpy-と-mainpy-を定義する)
  - [Router](#router)
    - [routerの実装](#routerの実装)
    - [スキーマの定義](#スキーマの定義)
  - [tips](#tips)
    - [dictの展開について](#dictの展開について)

---

## 概要

### **FastAPI**の特徴

- リクエストとレスポンスのスキーマ定義に合わせて自動的に Swagger UI のドキュメントが生成される
- 上記のスキーマを明示的に定義することにより、型安全な開発が可能
- ASGI（非同期サーバーゲートウェイインターフェース）に対応しているので、非同期処理を行うことができ、高速

スキーマを明示的に定義することによって、\
フロントエンドエンジニアが実装の際に利用するドキュメントを簡単に自動生成でき、\
さらに実際にリクエストパラメータを変更して API の呼び出しを試すこともできる。

→**スキーマ駆動開発**を自然的に始めることができる。

## 環境構築

Docker 環境を用意。\
詳細は、Dockerfile と docker-compose.yml を参照。

### **Poetry**とは

- Python のパッケージマネージャの一つ。Java における Maven のように、パッケージ同士の依存関係を解決する。
  > poetry では pip が行わないパッケージ同士の依存関係の解決や、lock ファイルを利用したバージョン固定、\
  > Python の仮想環境管理など、より高機能でモダンなバージョン管理が行えます。

**pyproject.toml**は、poetry において依存関係を管理するファイル。

### **Uvicorn**とは

> Uvicorn は uvloop と httptools を使った高速な ASGI サーバの実装です。\
> 最近まで Python には、asyncio フレームワークのための最小限の低レベルサーバー/アプリケーションインターフェースがありませんでした。ASGI 仕様はこのギャップを埋めるもので、すべての asyncio フレームワークで使える共通のツールセットを構築することができるようになりました。\
> ASGI は、Python の Web フレームワークのエコシステムを実現し、IO 負荷の高いコンテキストで高いスループットを達成するという点で、Node や Go に対して高い競争力を持つようになるはずです。また、WSGI では扱えない HTTP/2 や WebSocket への対応も行っています。\
> Uvicorn は現在、HTTP/1.1 と WebSocket をサポートしています。HTTP/2 への対応も予定されています。

### Poetry 定義ファイル作成

docker-compose build でイメージ作成後、下記コマンドで poetry の初期化、fastapi のインストールを行う。\
引数として、 fastapi と、ASGI サーバーである uvicorn をインストールする依存パッケージとして指定

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

### api ディレクトリ配下に、**init**.py と main.py を定義する

docker-compose up でコンテナ立ち上げ後、<http://localhost:8000/docs>にアクセスすると、\
Swagger UI が確認できる。実際にブラウザ上で定義した API を叩くことができる。

---

## Router

routers ディレクトリに、**パスオペレーション関数**を定義する。\
**パスオペレーション関数**は、REST API の「エンドポイント」と「HTTP メソッド」にそれぞれ対応します。

routersディレクトリにはリソースごとに、ファイルを分けるのが良さそう。

### routerの実装

```py
# /api/routers/task.py 抜粋
from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks")
async def list_tasks():
    pass
```

```py
# main.py 抜粋
from fastapi import FastAPI
from api.routers import task

app = FastAPI()

# routerインスタンスをfast apiインスタンスに取り込む
app.include_router(task.router)

```

### スキーマの定義

FastAPIでは、依存する**Pydantic**という強力なライブラリによって、\
型ヒントを積極的に利用し、 APIの入出力のバリデーション を行います。

```py
from typing import Optional

from pydantic import BaseModel, Field

# BaseModelクラスを継承
# 型を定義することで、バリデーションの役割を担う。
class Task(BaseModel):
    id: int
    title: Optional[str] = Field(None, example='クリーニングを取りに行く')
    done: bool = Field(False, description='完了フラグ')
```

---

## tips

### dictの展開について

```py
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    # dict インスタンスに対して先頭に ** をつけることで、 dict を キーワード引数として展開 し、
    # task_schema.TaskCreateResponse クラスのコストラクタに対して、\
    # dict のkey/valueを渡します。
    # つまり、task_schema.TaskCreateResponse(
    #         id=1,
    #         title=task_body.title,
    #         done=task_body.done
    #       ) と等価となります。
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())
```
