from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    try:
        response = requests.post(
            "https://api.fireworks.ai/inference/v1/chat/completions",
            headers={"Authorization": f"Bearer {FIREWORKS_API_KEY}"},
            json={
                "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
                "messages": [
                    {"role": "system", "content": "Ты помощник онлайн-магазина, помогай клиентам с покупками."},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        bot_response = response.json()
        return jsonify({"response": bot_response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": f"Ошибка: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

        
