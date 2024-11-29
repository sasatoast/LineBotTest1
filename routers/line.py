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

#新たな変数の宣言とライブラリの追加

from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    # access_token,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent

)
#エンドポイント作成のための新規ライブラリ
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from starlette.exceptions import HTTPException


#ここまで
load_dotenv()

router = APIRouter()
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
access_token = os.environ.get('CHANNEL_ACCESS_TOKEN')

@router.post(
    '/api/callback',
    summary='LINE Message APIからのコールバック',
    description='ユーザーからメッセージを受信した際、LINE Message APIからこちらにリクエストが送られます。',
)
async def callback(request: Request, x_line_signature=Header(None)):
    body = await request.body()
    

    try:
		# リクエストがLINEプラットフォームからのものかを検証する
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"

#エンドポイントの追加
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(access_token) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )
# # @handler.add(MessageEvent,message=TextMessage)#handler.ってなに？addって一般的なもの？
# def handle_message(event:MessageEvent): #eventだけじゃだめ?messageeventってなに？
#     print("event.message.text:{}".format(event.message.text))
#     with ApiClient(access_token) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=event.message.text),
#             )
from fastapi import (
    APIRouter,
    Header, 
    Request
)
import os
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler

# 以下のimportを追加
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
# ここまで
from starlette.exceptions import HTTPException

load_dotenv()
router = APIRouter()

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

# 以下の記述を追加
configuration = Configuration(access_token=os.environ.get('CHANNEL_ACCESS_TOKEN'))

@router.post(
    '/api/callback',
    summary='LINE Message APIからのコールバック',
    description='ユーザーからメッセージを受信した際、LINE Message APIからこちらにリクエストが送られます。',
)
async def callback(request: Request, background_tasks: BackgroundTasks, x_line_signature=Header(None)):
    body = await request.body()
    #requestは与えられた詳細な情報,awaitは非同期処理宣言であり
    #他のエンドポイントが作成された時にbody作成を待ってくれる

    try:
        background_tasks.add_task(
            handler.handle(body.decode("utf-8"), x_line_signature)
        )

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"

# 以下を追加
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )
