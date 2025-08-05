# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # ← CORSをインポート
from contextlib import asynccontextmanager
from typing import List, Optional
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from model import Todo, TodoBase, TodoUpdate, Subtask, SubtaskBase

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173", # ローカルReactサーバーのURL
    "https://todo-frontend-h062.onrender.com", # RenderでデプロイしたフロントエンドのURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# データベースセッションを取得するための依存関数
def get_session():
    with Session(engine) as session:
        yield session

# --- TODO API エンドポイント ---

@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoBase, session: Session = Depends(get_session)):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[Todo])
def read_todos(
    session: Session = Depends(get_session),
    search: Optional[str] = None
):
    query = select(Todo).order_by(Todo.created_at)
    if search:
        query = query.where(Todo.title.contains(search))
    todos = session.exec(query).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
        
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    session.delete(db_todo)
    session.commit()
    return {"message": "Todo deleted successfully"}

# --- Subtask API エンドポイント ---

@app.post("/todos/{todo_id}/subtasks/", response_model=Subtask)
def create_subtask_for_todo(
    todo_id: int, 
    subtask: SubtaskBase, 
    session: Session = Depends(get_session)
):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_subtask = Subtask.model_validate(subtask, update={"todo_id": todo_id})
    session.add(db_subtask)
    session.commit()
    session.refresh(db_subtask)
    return db_subtask

@app.get("/todos/{todo_id}/subtasks/", response_model=List[Subtask])
def read_subtasks_for_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return db_todo.subtasks