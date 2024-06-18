# web app
#flask(做程式, 架伺服器), django (django 一般是做網頁)


from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
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

app = Flask(__name__)

configuration = Configuration(access_token='AOpzWAOcbbH/0LQKIL55ph8VOfklsFEG8Weo8TuA2OUUQYtWmFIAttAxK3lN1BalfAQvqER+/zQgfUKc+w92hTbD9Fz5Lxw/HUbO39Jzl1Ua36lySFKmiGMCtF8n5wnfefQhe18k9OF8/d3T66rUJgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6cf61294a2a79e07aacd1c6ca4afbac2')

# 網址加/callback 才會執行此function
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        msg = event.message.text
        r = 'I dont understand'
        if msg in ['hi', 'Hi']:
            r = 'hi'
        elif msg == 'eat?':
            r = 'yet'
        elif msd in ['who are you', '你是誰']:
            r = 'robot'
        elif ['訂位', 'reservation'] in msg:
            r = 'did you wanna book a seat?'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=r)]
            )
        )

if __name__ == "__main__": # 確保程式是載入, 不是直接執行
    app.run()