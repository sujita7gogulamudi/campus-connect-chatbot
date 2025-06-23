from flask import Flask, render_template, request, jsonify
import sqlite3
from fuzzywuzzy import fuzz
import os

app = Flask(__name__)

def get_answer(user_input):
    # Connect to the SQLite database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    # Fetch all FAQs
    cursor.execute("SELECT question, answer FROM faqs")
    faqs = cursor.fetchall()
    conn.close()

    # Prepare user input
    user_input_clean = user_input.strip().lower()

    # Fuzzy match logic
    best_score = 0
    best_answer = "Sorry, I couldn't find an answer to that."

    for question, answer in faqs:
        score = fuzz.partial_ratio(user_input_clean, question.strip().lower())
        if score > best_score and score > 60:
            best_score = score
            best_answer = answer

    return best_answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    message = request.form['message']
    response = get_answer(message)
    return jsonify({'reply': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Required for Render
    app.run(host='0.0.0.0', port=port, debug=True)
