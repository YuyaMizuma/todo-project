from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class TodoBase(SQLModel):
    title: str = Field(index=True) #titleで検索するためにindex=Trueを追加
    deadline: Optional[datetime] = None
    memo: Optional[str] = None

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    #1つのTodoが複数のSubtaskを持つ関係性を定義
    subtasks: List["Subtask"] = Relationship(back_populates="todo")

class SubtaskBase(SQLModel):
    name: str

class Subtask(SubtaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #親であるTodoのIDを保存するための外部キー
    todo_id: Optional[int] = Field(default=None, foreign_key="todo.id")

    #Subtaskから親のTodoを参照するための関係性を定義
    todo: Optional[Todo] = Relationship(back_populates="subtasks")

# 更新時に受け取るデータモデル
# title, deadline, memoすべてが任意(Optional)
class TodoUpdate(SQLModel):
    title: Optional[str] = None
    deadline: Optional[datetime] = None
    memo: Optional[str] = None

# APIレスポンス用に、子タスクのリストを含むTodoモデルを定義
class TodoReadWithSubtasks(Todo):
    subtasks: List[Subtask] = []