from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS
import google.generativeai as genai  # Import Gemini API

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyB8CQ-EiOLdKKN7e6jMbDjhwG-Cttk3DlM"  # Replace with your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Function to fetch words with meanings related to a scenario using Gemini API
def get_words_with_meanings_for_scenario(scenario):
    """
    Uses the Gemini API to generate words with their meanings related to a specific scenario.
    
    Input:
        - scenario: A string representing the scenario (e.g., "airport").
    Returns:
        - A list of dictionaries containing words and their meanings.
    """
    try:
        # Create a prompt for the Gemini API
        prompt = f"Generate a list of 10 words related to {scenario} along with their meanings. Return the words and meanings in the following format: word - meaning."

        # Generate a response using the Gemini API
        response = model.generate_content(prompt)

        # Extract the generated text
        generated_text = response.text

        # Split the generated text into lines and process each line
        word_meanings = []
        for line in generated_text.split("\n"):
            if "-" in line:
                word, meaning = line.split("-", 1)  # Split on the first hyphen
                word_meanings.append({
                    "word": word.strip(),
                    "meaning": meaning.strip()
                })

        return word_meanings
    except Exception as e:
        print(f"Error generating words with meanings using Gemini API: {e}")
        return None

# API endpoint for scenarios
@app.route('/scenario', methods=['POST'])
def scenario():
    """
    API endpoint to get words with meanings related to a scenario using the Gemini API.
    """
    data = request.get_json()  # Get JSON data from the request
    scenario = data.get('place')  # Extract the scenario from the request

    if not scenario:
        return jsonify({'error': 'Scenario not provided'}), 400

    # Get words with meanings related to the scenario using the Gemini API
    word_meanings = get_words_with_meanings_for_scenario(scenario)

    if word_meanings:
        return jsonify({'words': word_meanings})
    else:
        return jsonify({'error': 'Failed to generate words for the scenario'}), 500

if __name__ == "__main__":
    app.run(debug=True)
