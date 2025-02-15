from flask import Flask, request, jsonify
import fireworks_sdk
import os

app = Flask(__name__)

# Получаем API-ключ Fireworks
api_key = os.getenv("FIREWORKS_API_KEY")
client = fireworks_sdk.Client(api_key=api_key)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    try:
        response = client.chat.completions.create(
            model="accounts/fireworks/models/llama-v2-7b-chat",
            messages=[
                {"role": "system", "content": "Ты помощник онлайн-магазина, помогай клиентам с покупками."},
                {"role": "user", "content": user_message}
            ]
        )

        # Исправленный блок проверки ответа Fireworks
        if not hasattr(response, "text") or not response.text:
            return jsonify({"error": "Ответ Fireworks пустой или неверный"}), 500

        bot_response = response.text  # Fireworks использует text, а не choices
        return jsonify({"response": bot_response})

    except fireworks_sdk.FireworksError as e:
        return jsonify({"error": f"Ошибка Fireworks AI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Неизвестная ошибка: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
        
