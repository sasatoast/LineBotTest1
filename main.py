from fastapi import FastAPI
# 追加
# lineファイルをインポート
import os
from api.routers import line

app = FastAPI()

# 追加
# lineファイルで定義したルートをアプリケーションに適用
app.include_router(line.router)

@app.get("/hello")
async def hello():
    print(f"CHANNEL_SECRET: {os.environ.get('CHANNEL_SECRET')}")

    return {"message": "hello world!"}
