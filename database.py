from sqlmodel import create_engine, SQLModel

#データベースファイルの名前を指定
sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

#データベースに接続するためのエンジンを作成
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    # model.pyで定義したモデルに基づいてテーブルを作成
    SQLModel.metadata.create_all(engine)