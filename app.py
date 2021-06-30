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
line_bot_api = LineBotApi('UUDxPaXsTJUudTQ/gUiKW9lnp4PUtfAaiRpkIWjKPZrDXHAiQb2+5BCDqB1Yp7D5DAnjhdhafiAvxjRbWX4U+cvAynf6Yb/gdJLuuxDvEh4gEiV3S/Bja3dl04Mm5nQ+fR4gCmihSZNKFuXvlghAzQdB04t89/1O/w1cDnyilFU=')
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