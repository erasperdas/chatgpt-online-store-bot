from flask import Flask, request, jsonify
import os
import fireworksdk

app = Flask(__name__)

api_key = os.getenv("FIREWORKS_API_KEY")
client = fireworksdk.Client(api_key=api_key)

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

           if not hasattr(response, "choices") or not response.choices:
            return jsonify({"error": "Ответ Fireworks пустой или неверный"}), 500

        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except fireworksdk.FireworkError as e:
        return jsonify({"error": f"Ошибка Fireworks AI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Неизвестная ошибка: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

        
