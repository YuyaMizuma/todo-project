import os # osをインポート
from sqlmodel import create_engine, SQLModel

# Renderが提供するDATABASE_URLを読み込む。なければNoneになる
database_url = os.getenv("DATABASE_URL")

# もしDATABASE_URLがなければ（ローカル環境）、SQLiteを使う
if not database_url:
    sqlite_file_name = "database.sqlite"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    # SQLiteを使う場合に必要な設定
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
else:
    # DATABASE_URLがあれば（Render環境）、PostgreSQLに接続
    engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)