import sqlite3

conn = sqlite3.connect('chatbot.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
''')

# Sample Q&A
faq_data = [
    ("When does semester 4 start?", "Semester 4 starts on July 10th."),
    ("How to contact placement cell?", "Email placements@yourcollege.edu."),
    ("What is the exam fee deadline?", "Exam fees must be paid by July 5th."),
    ("Where can I find the timetable?", "Check the student portal timetable section.")
]

cursor.executemany("INSERT INTO faqs (question, answer) VALUES (?, ?)", faq_data)
conn.commit()
conn.close()
