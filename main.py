from fastapi import FastAPI
# 追加
# lineファイルをインポート
import os
from api.routers.line import router

app = FastAPI()

# 追加
# lineファイルで定義したルートをアプリケーションに適用
app.include_router(router)
