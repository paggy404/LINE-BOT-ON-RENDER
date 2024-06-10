# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:40:37 2024

@author: USER
"""

from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction

import google.generativeai as genai


# 載入 LINE Message API 相關函式庫

import os
line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
handler = WebhookHandler(os.environ.get('Channel_Secret'))

api_key = 'AIzaSyBmmMTdKrkPrvIAFJHMzoY-hViCEWElZQQ'
genai.configure(api_key = api_key)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@傳送文字':
        try:
            message = TextSendMessage(  
                text = "我是 Linebot，\n您好！"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
    elif mtext == '醫生值班表':
        try:
            message = ImageSendMessage(
                original_content_url = "https://i.imgur.com/vVne59L.jpeg",
                preview_image_url = "https://i.imgur.com/vVne59L.jpeg"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    # 取出文字的前五個字元是 hi ai:
    elif mtext[:4] ==  '我不舒服':
        prompt="你是一個專業的皮膚科醫生，請用問診的方式幫我判斷我的皮膚有什麼症狀，根據以下內容給我溫柔平易近人回應:\n"+mtext[4:]
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        # try:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response.text))
        #     openai.api_key = openai.api_key(os.environ.get('Channel_API_keys'))
            # 將第六個字元之後的訊息發送給 OpenAI
        # except:
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))            

if __name__ == '__main__':
    app.run()
