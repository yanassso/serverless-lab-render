<<<<<<< HEAD
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/')
def hello():
	return "Hello, Serverless! 🚀"


@app.route('/echo', methods=['POST'])
def echo():
	# Получаем JSON из тела запроса
	data = request.get_json()

	# Если данных нет, возвращаем ошибку
	if data is None:
		return jsonify({"error": "No JSON data received"}), 400

	# Возвращаем полученные данные вместе с дополнительной информацией
	return jsonify({
		"status": "received",
		"you_sent": data,
		"length": len(str(data))
	})


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
=======

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Serverless! 🚀\n", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
>>>>>>> 6fa3a086e9e84fd7766f0cb74cdcf061373f2a6f
