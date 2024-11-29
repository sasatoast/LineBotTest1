from fastapi import FastAPI
# 追加
# lineファイルをインポート
# from .routers import line

app = FastAPI()

# 追加
# lineファイルで定義したルートをアプリケーションに適用
# app.include_router(line.router)

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}
