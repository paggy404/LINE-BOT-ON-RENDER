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

import openai


# 載入 LINE Message API 相關函式庫
import json

import os

line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
handler = WebhookHandler(os.environ.get('Channel_Secret'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
        handler = WebhookHandler('fb63a6a67e93c96b850177b269a0369b')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text']
        # 取出文字的前五個字元，轉換成小寫
        ai_msg = msg[:6].lower()
        reply_msg = ''
        # 取出文字的前五個字元是 hi ai:
        if ai_msg == '我不舒服':
            openai.api_key = 'sk-proj-0AgzlBVg2DDfSBLWkECkT3BlbkFJ29hyh38Vwbv89RujdEcV'
            # 將第六個字元之後的訊息發送給 OpenAI
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[6:],
                max_tokens=256,
                temperature=0.5,
                )
            # 接收到回覆訊息後，移除換行符號
            reply_msg = response["choices"][0]["text"].replace('\n','')
        else:
            reply_msg = msg
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)
    except:
        print('error')
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

    elif mtext == '@傳送貼圖':
        try:
            message = StickerSendMessage(  #貼圖兩個id需查表
                package_id='1',  
                sticker_id='2'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@多項傳送':
        try:
            message = [  #串列
                StickerSendMessage(  #傳送貼圖
                    package_id='1',  
                    sticker_id='2'
                ),
                TextSendMessage(  #傳送文字
                    text = "這是 Pizza 圖片！"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://i.imgur.com/4QfKuz1.png",
                    preview_image_url = "https://i.imgur.com/4QfKuz1.png"
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@傳送位置':
        try:
            message = LocationSendMessage(
                title='101大樓',
                address='台北市信義路五段7號',
                latitude=25.034207,  #緯度
                longitude=121.564590  #經度
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    if mtext == '@快速選單':
        try:
            message = TextSendMessage(
                text='請選擇最喜歡的程式語言',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="Python", text="Python")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="Java", text="Java")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="C#", text="C#")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="Basic", text="Basic")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
