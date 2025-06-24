from flask import Flask, render_template, request, jsonify
import sqlite3
from fuzzywuzzy import fuzz
import os
from transformers import pipeline
app = Flask(__name__)



# Load only once
gen_model = pipeline("text2text-generation", model="google/flan-t5-small")

def get_answer(user_input):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faqs")
    faqs = cursor.fetchall()
    conn.close()

    best_score = 0
    best_answer = None

    for question, answer in faqs:
        score = fuzz.partial_ratio(user_input.lower(), question.lower())
        if score > best_score and score > 60:
            best_score = score
            best_answer = answer

    if best_answer:
        return best_answer
    else:
        # Fallback to generative AI
        prompt = f"Answer this student question simply: {user_input}"
        result = gen_model(prompt, max_length=100, do_sample=True)[0]['generated_text']
        return result

# 🌐 Landing Page
@app.route('/')
def home():
    return render_template('index.html')

# 💬 Chat Page
@app.route('/chat')
def chat():
    return render_template('chat.html')  # move old index.html here as chat.html

# 📢 Notifications
@app.route('/dashboard')
def dashboard():
    return render_template('notifications.html')

# 📬 Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/links')
def links():
    return render_template('links.html')


# 💬 Chatbot Logic
@app.route('/ask', methods=['POST'])
def ask():
    message = request.form['message']
    response = get_answer(message)
    return jsonify({'reply': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
