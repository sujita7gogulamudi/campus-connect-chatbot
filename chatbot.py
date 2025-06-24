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


@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM notifications")
    notifications = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('dashboard.html', notifications=notifications)

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contact (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()
        return "Thanks for reaching out!"
    return render_template('contact.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Required for Render
    app.run(host='0.0.0.0', port=port, debug=True)
