import Database.models as m
from sqlalchemy.orm import Session
from Database.database import engine, session_local
from fastapi import FastAPI, Depends, HTTPException, status, Query, Path, APIRouter
from pydantic import BaseModel, Field
from typing import Annotated

route = APIRouter(prefix = "/home")


class Task_Modle(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(min_length=5, default="NA")
    assigned_to: str = Field(..., min_length=1)
    status: bool = Field(...)
    
    model_config= {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Give a title",
                    "description": "This is a description",
                    "assigned_to": "Taher Mulla",
                    "status": False,
                    "userId": "user@gmail.com"
                }
            ]
        }
    }

# insert into tasks (title, description, assigned_to, status) values ("Project", "Do the Fast API project", "TM", False)
# insert into tasks (title, description, assigned_to, status) values ("Cook Food", "Make something lite to eat", "TM", False)
# insert into tasks (title, description, assigned_to, status) values ("Eat food", "Eat a light dinner", "TM", False)
# insert into tasks (title, description, assigned_to, status) values ("Bath", "Have a bath", "TM", True)
# insert into tasks (title, description, assigned_to, status) values ("Mani", "Settle splitwise", "Mani", False)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
db_connection_dependancy = Annotated[Session, Depends(get_db)]
        
@route.get("/get_tasks")
def get_tasks(db: db_connection_dependancy):
    return db.query(m.Tasks).all()

@route.get("/get_number_of_tasks")
def get_tasks(db: db_connection_dependancy):
    return len(db.query(m.Tasks).all())

@route.get("/get_task_by_id", status_code=status.HTTP_200_OK)
def get_task_by_id(db: db_connection_dependancy, task_id: int = Query(gt=0)):
    task = db.query(m.Tasks).get(task_id)
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found, pls retry with different id")
    
    return task

@route.post("/add_task")
def add_task(db: db_connection_dependancy, task: Task_Modle):
    task = m.Tasks(**task.model_dump())
    db.add(task)
    db.commit()
    return 

@route.delete("/delete_task/{task_id}")
def delete_task(db: db_connection_dependancy, task_id: int = Path(gt=0)):  
    task = db.query(m.Tasks).filter(m.Tasks.id == task_id).first()
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provided ID dose not exist")
    
    db.delete(task)
    db.commit()
    
    return 

@route.put("/update_task/{task_id}")
def update_task(db: db_connection_dependancy, task: Task_Modle, task_id: int = Path(gt=0)):
    
    try:
        delete_task(db, task_id)
    except Exception as e:
        raise e
    
    task = m.Tasks(**task.model_dump())
    task.id = task_id
    
    db.add(task)
    db.commit()
    
    return 