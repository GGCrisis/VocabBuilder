from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

# Initialize the translator
translator = Translator()

def translate_text(text, target_language):
    """
    Translates text into the target language using googletrans.
    """
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        return f"Translation failed: {e}"

@app.route("/next_word", methods=["GET"])
def next_word():
    """
    Endpoint to fetch the next word and its meaning, and translate them.
    """
    # Fetch the next word and meaning from the database (replace with your database logic)
    word = "example"
    meaning = "a thing characteristic of its kind"

    # Get the selected language from the frontend (default to English if not provided)
    target_language = request.args.get("language", "en")

    # Translate the word and meaning
    translated_word = translate_text(word, target_language)
    translated_meaning = translate_text(meaning, target_language)

    return jsonify({
        "word": translated_word,
        "meaning": translated_meaning
    })

@app.route("/minigame/scenarios", methods=["POST"])
def scenarios():
    """
    Endpoint to fetch words for a specific place and translate them.
    """
    data = request.get_json()
    place = data.get("place")
    target_language = data.get("language", "en")  # Default to English if not provided

    if not place:
        return jsonify({"error": "Place not provided."}), 400

    # Fetch words related to the place from the database (replace with your database logic)
    words_data = [
        {"word": "example1", "meaning": "meaning1"},
        {"word": "example2", "meaning": "meaning2"}
    ]

    # Translate words and meanings
    translated_words = []
    for item in words_data:
        translated_word = translate_text(item["word"], target_language)
        translated_meaning = translate_text(item["meaning"], target_language)
        translated_words.append({
            "word": translated_word,
            "meaning": translated_meaning
        })

    return jsonify({"words": translated_words})

if __name__ == "__main__":
    app.run(debug=True)