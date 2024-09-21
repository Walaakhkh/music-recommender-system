#!/usr/bin/python3

from flask import Flask, jsonify, request
from musiccollaborativefiltering.recommender import ImplicitRecommender
from musiccollaborativefiltering.data import load_user_artists, ArtistRetriever
import implicit
import scipy
from pathlib import Path

app = Flask(__name__)

# Load user artists matrix and initialize recommender
user_artists = load_user_artists(Path("lastfmdata/user_artists.dat"))
artist_retriever = ArtistRetriever()
artist_retriever.load_artists(Path("lastfmdata/artists.dat"))
implicit_model = implicit.als.AlternatingLeastSquares(factors=50, iterations=10, regularization=0.01)
recommender = ImplicitRecommender(artist_retriever, implicit_model)
recommender.fit(user_artists)

@app.route('/recommend/<int:user_id>/<int:n>', methods=['GET'])
def get_recommendations(user_id: int, n: int):
    """Get recommendations for a specific user."""
    try:
        artists, scores = recommender.recommend(user_id, user_artists, n)
        return jsonify({"artists": artists, "scores": scores})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # Return error with status code 400

if __name__ == "__main__":
    app.run(port=5001)
