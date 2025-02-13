from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

OMDB_API_KEY = "b249dfe7"

# Load movie data & similarity matrix
movies = pickle.load(open("movie_list1.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_name):
    """Fetch movie poster from OMDb API"""
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    return response.get("Poster", "https://via.placeholder.com/300x450")  # Default if no poster found

def recommend(movie):
    """Return 5 recommended movies & their posters"""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    recommended_posters = []
    
    for i in distances[1:15]:  # Top 5 Recommendations
        movie_name = movies.iloc[i[0]].title
        recommended_movies.append(movie_name)
        recommended_posters.append(fetch_poster(movie_name))

    return recommended_movies, recommended_posters

@app.route("/", methods=["GET", "POST"])
def home():
    recommended_movies, recommended_posters = [], []
    
    if request.method == "POST":
        selected_movie = request.form.get("movie_name")
        recommended_movies, recommended_posters = recommend(selected_movie)
    
    return render_template("index.html", movie_list=movies["title"].values, recommendations=zip(recommended_movies, recommended_posters))

if __name__ == "__main__":
    app.run(debug=True)
