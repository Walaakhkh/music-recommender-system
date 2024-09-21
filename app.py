#!/usr/bin/python3

from flask import Flask, jsonify, request, render_template
from musiccollaborativefiltering.recommender import ImplicitRecommender
from musiccollaborativefiltering.data import load_user_artists, ArtistRetriever
import implicit
from pathlib import Path

app = Flask(__name__)

# Load user artists matrix and initialize recommender
user_artists = load_user_artists(Path("lastfmdata/user_artists.dat"))
artist_retriever = ArtistRetriever()
artist_retriever.load_artists(Path("lastfmdata/artists.dat"))
implicit_model = implicit.als.AlternatingLeastSquares(factors=50, iterations=10, regularization=0.01)
recommender = ImplicitRecommender(artist_retriever, implicit_model)
recommender.fit(user_artists)

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """Get recommendations for a specific user."""
    data = request.json
    user_id = int(data.get("user_id"))
    n = int(data.get("n"))
    try:
        artists, scores = recommender.recommend(user_id, user_artists, n)
        return jsonify({"artists": artists, "scores": scores})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)
