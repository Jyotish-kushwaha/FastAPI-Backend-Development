from fastapi import APIRouter , Depends, HTTPException , status
from src.tasks import controller
from src.tasks.dtos import TaskBody, TaskResponseSchema
from src.utils.db import get_db
from src.tasks.model import TaskModel
from typing import List

task_routes=APIRouter(prefix="/tasks")

@task_routes.post("/create",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def create_task(body:TaskBody, db=Depends(get_db)):
    print(body)
    return controller.create_task(body,db)

#return all data 
@task_routes.get("/all",response_model=List[TaskResponseSchema],status_code=status.HTTP_200_OK)
def get_tasks(db=Depends(get_db)):
    return controller.get_tasks(db)

# return unique ele
@task_routes.get("/{id}",response_model=TaskResponseSchema,status_code=status.HTTP_200_OK)
def get_task(id:int,db=Depends(get_db)):
    return controller.get_task(id,db)

# update the task
@task_routes.put("/update/{id}",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def update_task(id:int,body:TaskBody,db=Depends(get_db)):
    return controller.update_task(id,body,db)

@task_routes.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int,db=Depends(get_db)):
    return controller.delete_task(id,db)