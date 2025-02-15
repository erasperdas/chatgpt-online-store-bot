from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помощник онлайн-магазина, помогай клиентам с покупками."},
            {"role": "user", "content": user_message}
        ]
    )
    bot_response = response["choices"][0]["message"]["content"]
    return jsonify({"response": bot_response})

if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
