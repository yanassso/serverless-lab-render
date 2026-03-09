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
