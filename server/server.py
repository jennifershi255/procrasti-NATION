# Flask Server
import cohere
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from db import get_database
from datetime import datetime
from classifier import classify

# load environment variables from .env file
load_dotenv()

# Retrives API key for Cohere from the environment variables
api_key = os.getenv("API_KEY")
co = cohere.Client(api_key=api_key)

app = Flask(__name__)
CORS(app)

@app.route('/excuse', methods=['POST'])
def excuses():
    data = request.get_json() # converts incoming JSON into a python dictionary
    task = data['task']
    excuse_type = data['type_of_res'] #type_of_res refers to 

    response = co.chat(
        model="command-r-plus",
        message=f"Provide a single custom sarcastic, realistic {excuse_type} excuse that the user can use to avoid doing their {task}. Make sure the excuse is less than 30 words in length. Use 'my productivity is solar-powered, and unfortunately, it's cloudy today' as an example of an absurd excuse. Use science for scientific excuses. don't always start sentences with 'sorry, I can't.",
    )
    try:
        urgency = classify([task]).classifications[0].prediction
        db = get_database()
        history_collection = db['history']
        now = datetime.now().strftime("%Y-%m-%d")
        # stores request in database
        history_collection.insert_one({"task": task, "urgency": urgency, "date": now, "response": response.text})
    except:
        return jsonify({"response" : response.text, "urgency": "unknown"})
    return jsonify({"response" : response.text, "urgency": urgency})

# Retrieves past excuse data
@app.route('/history', methods=['GET'])
def history_function():
    db = get_database()
    history_collection = db['history']
    history = list(history_collection.find())  # Returns a cursor object
    needed_history = []
    for h in history:
        h['_id'] = str(h['_id'])
        needed_history.append(h)
    needed_history = sorted(needed_history, key=lambda x: x['date'], reverse=True)
    all_history = {"history": needed_history}
    return jsonify(all_history)


if __name__ == '__main__':
    app.run(debug=True)
    