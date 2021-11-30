from typing import List
from fastapi import APIRouter
import api.schemas.task as task_schema

router = APIRouter()


@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title='1つ目のTodoタスク')]


@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    # dict インスタンスに対して先頭に ** をつけることで、 dict を キーワード引数として展開 し、
    # task_schema.TaskCreateResponse クラスのコストラクタに対して dict のkey/valueを渡します。
    # つまり、task_schema.TaskCreateResponse(id=1, title=task_body.title, done=task_body.done) と等価となります。
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())


@router.put("/tasks/{task_id}")
async def update_task():
    pass


@router.delete("tasks/{task_id}")
async def delete_task():
    pass
