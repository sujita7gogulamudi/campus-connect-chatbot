import csv
import sqlite3

conn = sqlite3.connect('chatbot.db')
cursor = conn.cursor()

# FAQs
cursor.execute('DROP TABLE IF EXISTS faqs')
cursor.execute('''
    CREATE TABLE faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
''')

with open('data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    next(reader)  # Skip header
    for row in reader:
        if len(row) >= 2:
            question = row[0].strip()
            answer = ','.join(row[1:]).strip()
            cursor.execute('INSERT INTO faqs (question, answer) VALUES (?, ?)', (question, answer))

# Notifications
cursor.execute('DROP TABLE IF EXISTS notifications')
cursor.execute('''
    CREATE TABLE notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL
    )
''')

sample_notifications = [
    ("Semester 4 classes begin July 10."),
    ("Revaluation deadline is July 5."),
    ("Placement drive starts August 1.")
]

cursor.executemany("INSERT INTO notifications (message) VALUES (?)", [(n,) for n in sample_notifications])

# Contact Us Form
cursor.execute('DROP TABLE IF EXISTS contact')
cursor.execute('''
    CREATE TABLE contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("✅ Database created successfully from data.csv + notifications + contact table")
