#!/usr/bin/python3
"""
 API endpoint in your backend that returns the music recommendations
 """

 from flask import Flask, jsonify

app = Flask(__name__)

# Dummy function to simulate recommendations
def get_recommendations(user_id):
    return [
        {"artist": "Artist A", "score": 0.95},
        {"artist": "Artist B", "score": 0.92},
        {"artist": "Artist C", "score": 0.89},
        {"artist": "Artist D", "score": 0.87},
    ]

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    try:
        recommendations = get_recommendations(user_id)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
