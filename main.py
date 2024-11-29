from fastapi import FastAPI

#routersの接続
from routers import line
app = FastAPI()
# lineファイルで定義したルートをアプリケーションに適用
app.include_router(line.router)


@app.get("/hello")
async def hello():
    return{"message":"hello world!"}
