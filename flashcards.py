import psycopg2
from plyer import notification
from datetime import date
from flask import Flask, jsonify
from flask_cors import CORS  # Add CORS support

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",  # Change if necessary
    database="Vocab",  # Your PostgreSQL database name
    user="postgres",  # Your PostgreSQL username
    password="123456"  # Your PostgreSQL password
)
cursor = conn.cursor()

# Function to get the next word and its meaning
def get_next_word_and_meaning():
    """
    Fetches the next word from the database.
    """
    cursor.execute("SELECT id, word, meaning FROM words WHERE displayed IS NULL LIMIT 1")
    next_word_row = cursor.fetchone()  # Fetch the next word

    if next_word_row:
        word = next_word_row[1]  # Word is in column 1
        meaning = next_word_row[2]  # Meaning is in column 2
        word_id = next_word_row[0]  # ID is in column 0

        # Mark this word as displayed by setting the 'displayed' column to today's date
        cursor.execute("UPDATE words SET displayed = %s WHERE id = %s", (str(date.today()), word_id))
        conn.commit()

        return (word, meaning, word_id)
    else:
        # If no more words are available to show
        print("No more words left in the database.")
        return None

# Function to send notification (desktop notification)
def send_notification(word, meaning):
    """
    Sends a desktop notification with the word and its meaning.
    """
    notification.notify(title=word, message=meaning)

@app.route('/next_word', methods=['GET'])
def next_word():
    """
    API endpoint to get the next word and meaning.
    """
    word_data = get_next_word_and_meaning()
    if word_data:
        word, meaning, word_id = word_data
        send_notification(word, meaning)  # Send the notification
        return jsonify({'word': word, 'meaning': meaning})
    else:
        return jsonify({'message': 'No more words left to display.'}), 404

if __name__ == "__main__":
    app.run(debug=True)
    
    
