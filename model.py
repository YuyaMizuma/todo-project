# model.py

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone # timezoneもインポート

# --- APIで受け取るデータの「形」を定義するベースモデル ---

class TodoBase(SQLModel):
    title: str

class SubtaskBase(SQLModel):
    name: str

# PATCHリクエストで更新するデータ用のモデル
class TodoUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

# --- データベースの「テーブル」を定義するモデル ---

# Subtaskテーブル
# 「どのTodoに属しているか」という情報を持つ
class Subtask(SubtaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    todo_id: Optional[int] = Field(default=None, foreign_key="todo.id")
    
    # Subtaskから親のTodoを参照するための関連付け
    todo: Optional["Todo"] = Relationship(back_populates="subtasks")

# Todoテーブル
# 「どんなSubtaskを持っているか」という情報を持つ
class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    completed: bool = False
    # default_factoryを使って、現在時刻を自動で設定
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Todoから子要素のSubtaskリストを参照するための関連付け
    subtasks: List[Subtask] = Relationship(back_populates="todo")


# --- APIが返す「レスポンス」の形を定義するモデル ---

# 子タスクを含まない、基本的なTodoのレスポンス用
class TodoRead(TodoBase):
    id: int
    completed: bool
    created_at: datetime

# 子タスクのリストを含む、Todoのレスポンス用
# ★これが今回の修正の核となる部分です
class TodoReadWithSubtasks(TodoRead):
    subtasks: List[Subtask] = []