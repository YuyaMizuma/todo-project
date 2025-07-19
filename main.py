from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables

# FastAPIアプリが起動したときに一度だけ実行される処理を定義
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    create_db_and_tables()
    yield

# lifespanをFastAPIアプリに登録
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
