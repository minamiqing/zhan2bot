import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取 Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# 初始化 Flask 应用
app = Flask(__name__)

# 主页路由（检查用）
@app.route("/", methods=["GET"])
def index():
    return "湛湛2号系统运行中。"

# Webhook 路由，接收 Telegram 消息
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("收到数据：", data)  # 调试输出

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if chat_id and text:
        send_message(chat_id, f"你说了: {text}")

    return "OK"

# 发送消息函数
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    return response.json()

# 启动 Flask 服务
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

