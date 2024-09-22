# This music recommendation system readme file

## Overview
This project is a music recommender system that uses collaborative filtering techniques to recommend artists to users based on their listening history.

## Project Structure
- `recommender-backend/`: Backend logic for the recommender system.
- `lastfmdata/`: Data files containing user and artist information.
- `recommender_api.py`: Flask API to interact with the recommender system.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
4. Place your `user_artists.dat` and `artists.dat` files in the `lastfmdata/` directory.

# Run poetry
poetry install

## Running the API
Run the Flask API:
```bash
python recommender_api.py
