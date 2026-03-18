import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище сообщений в памяти
messages = []
ACCESS_PASSWORD = "00000"

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    # Проверка пароля прямо при отправке
    if not data or data.get("password") != ACCESS_PASSWORD:
        return jsonify({"status": "error", "message": "Forbidden"}), 403
    
    if 'user' in data and 'text' in data:
        messages.append({"user": data['user'], "text": data['text']})
        # Ограничиваем историю (последние 100 сообщений)
        if len(messages) > 100:
            messages.pop(0)
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/get', methods=['GET'])
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    # Порт для Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
