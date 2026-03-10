from flask import Flask, request, jsonify
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Подключение к БД
DATABASE_URL = os.environ.get('DATABASE_URL')
conn = None

if DATABASE_URL:
	try:
		url = urlparse(DATABASE_URL)
		conn = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		# Создание таблицы при старте
		with conn.cursor() as cur:
			cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
			conn.commit()
		print("✅ База данных подключена и готова к работе")
	except Exception as e:
		print(f"❌ Ошибка подключения к БД: {e}")


@app.route('/')
def hello():
	return "Hello, Serverless! 🚀\n", 200, {'Content-Type': 'text/plain'}


@app.route('/echo', methods=['POST'])
def echo():
	data = request.get_json()
	return jsonify({
		"status": "received",
		"you_sent": data,
		"length": len(str(data)) if data else 0
	})


@app.route('/save', methods=['POST'])
def save_message():
	if not conn:
		return jsonify({"error": "DB not connected"}), 500

	try:
		data = request.get_json()
		message = data.get('message', '') if data else ''

		with conn.cursor() as cur:
			cur.execute("INSERT INTO messages (content) VALUES (%s) RETURNING id", (message,))
			msg_id = cur.fetchone()[0]
			conn.commit()

		return jsonify({"status": "saved", "id": msg_id, "message": message})
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@app.route('/messages')
def get_messages():
	if not conn:
		return jsonify({"error": "DB not connected"}), 500

	try:
		with conn.cursor() as cur:
			cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC LIMIT 10")
			rows = cur.fetchall()

		messages = [{"id": r[0], "text": r[1], "time": r[2].isoformat()} for r in rows]
		return jsonify(messages)
	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Serverless! 🚀\n", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

