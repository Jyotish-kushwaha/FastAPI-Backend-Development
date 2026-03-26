from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.tasks.dtos import TaskBody , TaskResponseSchema
from src.utils.db import get_db
from src.tasks.model import TaskModel


def create_task(body:TaskBody ,db=Session):
    data=body.model_dump()
    new_task=TaskModel(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"]
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db=Session):
    data=db.query(TaskModel).all()
    return data

def get_task(id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not task:
        return {"error": "Task not found"}

    return task
    
def update_task(id: int, body: TaskBody, db: Session):
    task = db.get(TaskModel, id)   # better than .query().get()

    if not task:
        raise HTTPException(status_code=404, detail="not found")

    update_data = body.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task(id:int,db:Session):
    task=db.query(TaskModel).filter(TaskModel.id==id).first()
    if not task:
        raise HTTPException(status_code=404,detail="not found")
    db.delete(task)
    db.commit()
    return None


