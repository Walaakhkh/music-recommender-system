#!/usr/bin/python3
# recommender_api.py

from flask import Flask, request, jsonify
from recommenderbackend.recommender import ImplicitRecommender
from recommenderbackend.data import load_user_artists, ArtistRetriever
from pathlib import Path
import implicit
import logging

# Initialize the Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load data
try:
    user_artists_path = Path("lastfmdata/user_artists.dat")
    artist_data_path = Path("lastfmdata/artists.dat")
    
    app.logger.info(f"Loading user artists from {user_artists_path}")
    user_artists = load_user_artists(user_artists_path)

    app.logger.info(f"Loading artist data from {artist_data_path}")
    artist_retriever = ArtistRetriever()
    artist_retriever.load_artists(artist_data_path)
except Exception as e:
    app.logger.error(f"Error loading data: {e}")
    raise

# Initialize the ALS model and the recommender
try:
    app.logger.info("Initializing the ALS model and recommender")
    model = implicit.als.AlternatingLeastSquares(factors=50, iterations=10, regularization=0.01)
    recommender = ImplicitRecommender(artist_retriever, model)
    recommender.fit(user_artists)
except Exception as e:
    app.logger.error(f"Error initializing the recommender: {e}")
    raise

# Serve the frontend page
@app.route('/')
def home():
    try:
        return app.send_static_file('index.html')
    except Exception as e:
        app.logger.error(f"Error serving index.html: {e}")
        return jsonify({"error": "Failed to load homepage"}), 500

# Recommendation endpoint
@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        user_id = int(request.args.get('user_id', 1))  # Default user_id to 1
        n = int(request.args.get('n', 5))  # Default number of recommendations to 5

        app.logger.debug(f"Received request for user_id={user_id} and n={n}")
        
        artists, scores = recommender.recommend(user_id, user_artists, n=n)

        # Return the recommendations as a JSON response
        return jsonify({
            "user_id": user_id,
            "recommendations": [{"artist": artist, "score": score} for artist, score in zip(artists, scores)]
        })

    except ValueError as ve:
        app.logger.error(f"ValueError: {ve}")
        return jsonify({"error": "Invalid input, please check user_id and n"}), 400
    except Exception as e:
        app.logger.error(f"Error during recommendation: {e}")
        return jsonify({"error": "An error occurred during recommendation"}), 500

if _name_ == "_main_":
    try:
        app.logger.info("Starting the Flask application on port 5002")
        app.run(debug=True, port=5002)
    except Exception as e:
        app.logger.error(f"Error starting the Flask app: {e}")
