# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 00:43:01 2024

@author: USER
"""

import openai

from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi('iEVdKuc1rIeUrDXqFKWC0sfeBm20ffPTBuUPXOdcwbTqgFhkwPYy2PZwgjLzc09wYYkEtGKJLzlR+1GmzujUcHBVHceVrtNig42wTQ6Lu4rctDQ+5cJnL2PedQRsfq/kPIwWLCkgpgPhBbG81QGoSwdB04t89/1O/w1cDnyilFU=')
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

if __name__ == '__main__':
    app.run()
