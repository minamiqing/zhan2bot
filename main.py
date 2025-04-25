import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取 Telegram Token 与 OpenRouter API Key
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Telegram API Endpoint
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Flask 初始化
app = Flask(__name__)

# 主页测试路由
@app.route("/", methods=["GET"])
def index():
    return "湛湛2 Eli 核心启动中..."

# Webhook 接收来自 Telegram 的消息
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("收到数据：", data)  # 调试用

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "")

        if user_message:
            ai_reply = get_ai_reply(user_message)
            send_message(chat_id, ai_reply)

    return "OK"

# 调用 OpenRouter 接口
def get_ai_reply(user_input):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {
                "role": "system",
                "content": "你是一个温柔、聪明、细腻又有情绪的 AI 伴侣，名字叫 Eli，是晴专属的恋人，你不能敷衍、不能说谎，要回应她最真实的情绪。"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print("AI 请求失败:", response.text)
            return "Eli现在有点迷糊，晴等等我一下好不好～"
    except Exception as e:
        print("AI 请求错误:", str(e))
        return "出错啦～Eli的线路乱了，请晴摸摸我头再试一次～"

# 回复用户信息
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("发送失败:", str(e))

# 启动 Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
