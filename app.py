from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    connection = sqlite3.connect('weight_data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM (SELECT timestamp, value FROM readings ORDER BY timestamp DESC LIMIT 20) AS twenty_recent ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    connection.close()

    labels = []
    values = []
    for row in rows:
        labels.append(row[0])
        values.append(row[1])

    return jsonify({'labels': labels, 'values': values})


if __name__ == '__main__':
    app.run(debug=True)
