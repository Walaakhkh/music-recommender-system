#!/usr/bin/python3
#A simple Flask API for recommending artists using implicit recommender system

# Import necessary libraries and modules
from flask import Flask, request, jsonify
from recommenderbackend.recommender import ImplicitRecommender
from recommenderbackend.data import load_user_artists, ArtistRetriever      
from pathlib import Path
import implicit

# Create an instance of the Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Load data
user_artists = load_user_artists(Path("lastfmdata/user_artists.dat"))
artist_retriever = ArtistRetriever()
artist_retriever.load_artists(Path("lastfmdata/artists.dat"))

# Initialize the model
model = implicit.als.AlternatingLeastSquares(factors=50, iterations=10, regularization=0.01)
recommender = ImplicitRecommender(artist_retriever, model)
recommender.fit(user_artists)

# Define a route for the home page, serving the static 'index.html' file
@app.route('/')
def home():
    return app.send_static_file('index.html')

# Define a route for generating artist recommendations based on user ID
@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = int(request.args.get('user_id', 1))  # Get user ID from query parameter
    n = int(request.args.get('n', 5))  # Number of recommendations
    artists, scores = recommender.recommend(user_id, user_artists, n=n)

    # Return the recommendations as a JSON response
    return jsonify({
        "user_id": user_id,
        "recommendations": [{"artist": artist, "score": score} for artist, score in zip(artists, scores)]
    })

# Run the Flask app on port 5002
if __name__ == "__main__":
    app.run(debug=True, port=5002)
