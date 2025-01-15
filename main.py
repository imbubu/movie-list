from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# File to store movies
MOVIE_FILE = 'movies.json'

# Load movies from the JSON file
def load_movies():
    if os.path.exists(MOVIE_FILE):
        with open(MOVIE_FILE, 'r') as f:
            return json.load(f)
    return []

# Save movies to the JSON file
def save_movies(movies):
    with open(MOVIE_FILE, 'w') as f:
        json.dump(movies, f)

@app.route('/')
def index():
    movies = load_movies()
    return render_template('index.html', movies=movies)

@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.json
    movies = load_movies()
    movies.append({'title': data['title'], 'year': data['year'], 'rating': 0})
    save_movies(movies)
    return jsonify({'message': 'Movie added successfully!'}), 201

@app.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(index):
    movies = load_movies()
    if 0 <= index < len(movies):
        movies.pop(index)
        save_movies(movies)
        return jsonify({'message': 'Movie deleted successfully!'}), 204
    return jsonify({'message': 'Movie not found!'}), 404

@app.route('/movies/<int:index>', methods=['PUT'])
def edit_movie(index):
    data = request.json
    movies = load_movies()
    if 0 <= index < len(movies):
        movies[index]['title'] = data['title']
        movies[index]['year'] = data['year']
        save_movies(movies)
        return jsonify({'message': 'Movie updated successfully!'}), 200
    return jsonify({'message': 'Movie not found!'}), 404

@app.route('/movies/rate/<int:index>', methods=['POST'])
def rate_movie(index):
    data = request.json
    movies = load_movies()
    if 0 <= index < len(movies):
        movies[index]['rating'] = data['rating']
        save_movies(movies)
        return jsonify({'message': 'Rating updated successfully!'}), 200
    return jsonify({'message': 'Movie not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)