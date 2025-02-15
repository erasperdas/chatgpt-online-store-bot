from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Создаем клиента OpenAI с новой версией API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Получаем сообщение от пользователя
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "Сообщение не может быть пустым"}), 400

        # Отправляем запрос в OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник онлайн-магазина, помогай клиентам с покупками."},
                {"role": "user", "content": user_message}
            ]
        )

        # Получаем ответ от модели
        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except openai.APIError as e:  # Исправлено!
        return jsonify({"error": f"Ошибка OpenAI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Неизвестная ошибка: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

        
