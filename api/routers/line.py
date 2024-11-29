from fastapi import (
    APIRouter,
    Header, 
    Request
)
import os
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from starlette.exceptions import HTTPException

load_dotenv()
router = APIRouter()

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

@router.post(
    '/api/callback',
    summary='LINE Message APIからのコールバック',
    description='ユーザーからメッセージを受信した際、LINE Message APIからこちらにリクエストが送られます。',
)
async def callback(request: Request):
    body = await request.body()

    try:
		# リクエストがLINEプラットフォームからのものかを検証する
        handler.handle(body.decode("utf-8"))

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"