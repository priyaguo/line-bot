from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#Channel access token
line_bot_api = LineBotApi('lSCNLUwIax56RtzAM+mGCx2MJOiRM6K+Zgf4gGY7dbeb9Ud9spglR6WsOv22n1dCDAnjhdhafiAvxjRbWX4U+cvAynf6Yb/gdJLuuxDvEh6HQ3kCGPykdp8oThyP+aat1ubfXL/nAj7nNYmDJ4zPPQdB04t89/1O/w1cDnyilFU=')
#Channel secret
handler = WebhookHandler('35991513ba439437bbda73f20ca568ea')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()