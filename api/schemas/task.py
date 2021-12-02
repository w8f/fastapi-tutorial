from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example='クリーニングを取りに行く')


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    done: bool = Field(False, description='完了フラグ')

    class Config:
        orm_mode = True


class TaskCreateResponse(TaskCreate):
    id: int

    # orm_mode = True は、このレスポンススキーマ TaskCreateResponse が、
    # 暗黙的にORMを受け取り、レスポンススキーマに変換することを意味する。
    class Config:
        orm_mode = True
