from flask import Flask, request, jsonify, render_template
import requests
import random

app = Flask(__name__)

# Gemini API Key and Endpoint (replace with actual values)
GEMINI_API_KEY = "AIzaSyB8CQ-EiOLdKKN7e6jMbDjhwG-Cttk3DlM"
GEMINI_ENDPOINT = "https://api.gemini.com/v1/words"

@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


@app.route("/minigame/speed", methods=["GET"])
def speed_game():
    """Speed game endpoint."""
    try:
        # Fetch words from the Gemini API
        response = requests.get(
            f"{GEMINI_ENDPOINT}/speed",
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"}
        )
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Parse words and meanings from API response
        words_data = data.get("words", [])
        if not words_data:
            return render_template("error.html", message="No words available for the game.")

        # Prepare word-meaning pairs
        words_meanings = [
            {"word": item.get("word", "Unknown"), "meaning": item.get("meaning", "No meaning available")}
            for item in words_data
        ]

        # Shuffle the list for randomness
        random.shuffle(words_meanings)

        # Render the speed game page with the words and meanings
        return render_template("speed_game.html", words_meanings=words_meanings)

    except requests.exceptions.RequestException as e:
        # Handle API request errors
        return render_template("error.html", message=f"Error fetching words: {e}")
    except Exception as e:
        # Handle unexpected errors
        return render_template("error.html", message=f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app.run(debug=True)


#---------------------- Pronunciation Game --------------------------------------
@app.route("/minigame/pronunciation", methods=["GET"])
def pronunciation_game():
    try:
        response = requests.get(
            f"{GEMINI_ENDPOINT}/pronunciation", 
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"}
        )
        response.raise_for_status()
        data = response.json()
        words_data = data.get("words", [])
        
        if not words_data:
            return jsonify({"message": "No words for pronunciation available."})
        
        words = []
        for item in words_data:
            if isinstance(item, dict) and 'word' in item:
                words.append(item['word'])
        
        return render_template('pronunciation_game.html', words = words) 
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Error fetching words: {e}"}), 500
    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500

#---------------------- Scenarios Game ----------------------------------------
@app.route("/minigame/scenarios", methods=["POST"])
def scenarios_game():
    data = request.get_json()
    place = data.get("place", "").lower()

    try:
        response = requests.post(
            GEMINI_ENDPOINT,
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={"place": place}
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()
        words = response_data.get("words", ["No words found."])
    except requests.exceptions.RequestException as e:
         print(f"Error during request: {e}")
         words = ["Error fetching words from Gemini API"]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        words = ["An unexpected error occurred"]

    return jsonify({"words": words})

if __name__ == "__main__":
    app.run(debug=True)
