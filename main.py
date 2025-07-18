from fastapi import FastAPI

app = FastAPI()


# 返り値の型ヒントを記述
@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
