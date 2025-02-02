from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
import random
import time

app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_NAME = "Speed"
DB_USER = "postgres"
DB_PASSWORD = "123456"

# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")

@app.route("/minigame/speed", methods=["GET"])
def speed_game():
    """Speed game endpoint."""
    try:
        # Fetch words and meanings from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT word, meaning FROM words WHERE displayed = TRUE")
        words_data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not words_data:
            return jsonify({"error": "No words available for the game."}), 404

        # Prepare word-meaning pairs
        words_meanings = [{"word": item[0], "meaning": item[1]} for item in words_data]

        # Shuffle the list for randomness
        random.shuffle(words_meanings)

        # Return the words and meanings as JSON
        return jsonify({"words_meanings": words_meanings})

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route("/minigame/speed/submit", methods=["POST"])
def speed_game_submit():
    """Submit the user's matched words."""
    start_time = time.time()  # Start the timer when game begins

    # Get the data from the form submission
    matched_words = request.form.getlist("matched_words")  # List of matched word-meaning pairs

    # Add game logic: check if the user's matches are correct
    correct_matches = 0
    for word in matched_words:
        # Split word-meaning pair
        word, meaning = word.split(":")
        # Check if the match is correct (you might want to check the database to verify correctness)
        # For simplicity, we'll assume the match is correct for now.

        correct_matches += 1  # Assuming user matched it correctly

    elapsed_time = time.time() - start_time
    if elapsed_time < 120:  # Timer is less than 2 minutes
        return redirect(url_for("speed_game"))  # Proceed to the next set of words

    return render_template("home.html", message=f"Game Over! You matched {correct_matches} words.")

@app.route("/scenario", methods=["POST"])
def scenario():
    """Scenario endpoint to fetch words for a specific place."""
    try:
        data = request.get_json()
        place = data.get("place")

        if not place:
            return jsonify({"error": "Place not provided."}), 400

        # Fetch words related to the place from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT word, meaning FROM words WHERE category = %s", (place,))
        words_data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not words_data:
            return jsonify({"error": f"No words found for the place: {place}."}), 404

        # Prepare word-meaning pairs
        words = [{"word": item[0], "meaning": item[1]} for item in words_data]

        return jsonify({"words": words})

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)