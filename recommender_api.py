#!/usr/bin/python3
# recommender_api.py

from flask import Flask, request, jsonify
from recommenderbackend.recommender import ImplicitRecommender
from recommenderbackend.data import load_user_artists, ArtistRetriever
from pathlib import Path
import implicit

app = Flask(_name_, static_folder='frontend', static_url_path='')

# Load data
user_artists = load_user_artists(Path("lastfmdata/user_artists.csv"))
artist_retriever = ArtistRetriever()
artist_retriever.load_artists(Path("lastfmdata/artists.csv"))

# Initialize the model
model = implicit.als.AlternatingLeastSquares(factors=50)
recommender = ImplicitRecommender(artist_retriever, model)
recommender.fit(user_artists)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = int(request.args.get('user_id', 1))
    n = int(request.args.get('n', 5))  # Number of recommendations
    artists, scores = recommender.recommend(user_id, n)

    # Return the recommendations as a JSON response
    return jsonify({
        "user_id": user_id,
        "recommendations": [{"artist": artist, "score": score} for artist, score in zip(artists, scores)]
    })

if _name_ == "_main_":
    app.run(debug=True, port=5002)
