# database.py
import os
from sqlmodel import create_engine, SQLModel

database_url = os.getenv("DATABASE_URL")

# RenderのPostgreSQL URLをSQLAlchemyが認識できる形式に修正
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://")

# もしDATABASE_URLがなければ（ローカル環境）、SQLiteを使う
if not database_url:
    sqlite_file_name = "database.sqlite"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
else:
    # DATABASE_URLがあれば（Render環境）、PostgreSQLに接続
    engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)