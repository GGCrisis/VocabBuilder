from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Mock database of words and meanings (replace with your actual database logic)
WORDS_DATABASE = [
    {"word": "example", "meaning": "a thing characteristic of its kind"},
    {"word": "apple", "meaning": "a fruit that grows on trees"},
    {"word": "book", "meaning": "a written or printed work consisting of pages glued together"},
    {"word": "computer", "meaning": "an electronic device for storing and processing data"},
]

def translate_text(text, target_language):
    """
    Translates text into the target language using deep_translator.
    """
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation
    except Exception as e:
        return f"Translation failed: {e}"

@app.route("/next_word", methods=["GET"])
def next_word():
    """
    Endpoint to fetch the next word and its meaning, and translate them.
    """
    # Get the selected language from the frontend (default to English if not provided)
    target_language = request.args.get("language", "en")

    # Fetch the next word and meaning from the database (mock logic)
    if not hasattr(next_word, "index"):
        next_word.index = 0  # Initialize index for tracking the next word

    if next_word.index >= len(WORDS_DATABASE):
        next_word.index = 0  # Reset index if we've reached the end of the database

    word_data = WORDS_DATABASE[next_word.index]
    next_word.index += 1  # Move to the next word for the next request

    # Translate the word and meaning
    translated_word = translate_text(word_data["word"], target_language)
    translated_meaning = translate_text(word_data["meaning"], target_language)

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

    # Fetch words related to the place from the database (mock logic)
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