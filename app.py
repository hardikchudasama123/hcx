import pickle
import streamlit as st
import requests
from requests.utils import quote

# OMDb API se movie poster fetch karne ka function
def fetch_poster(movie_name):
    API_KEY = "b249dfe7"  # Tumhari API key
    encoded_name = quote(movie_name)
    url = f"http://www.omdbapi.com/?t={encoded_name}&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except requests.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"
    
    if data.get("Response") == "True" and "Poster" in data and data["Poster"] != "N/A":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in distances[1:11]:  # Top 10 recommendations
            movie_name = movies.iloc[i[0]].title
            recommended_movie_names.append(movie_name)
            recommended_movie_posters.append(fetch_poster(movie_name))
        
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return [], []

# Streamlit UI
st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.header('🎬 Movie Recommender System')

# Load model
try:
    movies = pickle.load(open('movie_list1.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("⚠️ Required files not found! Please check 'movie_list1.pkl' and 'similarity.pkl'.")
    st.stop()

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Type or select a movie from the dropdown", movie_list)

# Show recommendations
if st.button('🎥 Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    if recommended_movie_names:
        # 🔹 First Row (5 Movies)
        cols1 = st.columns(5)
        for col, name, poster in zip(cols1, recommended_movie_names[:5], recommended_movie_posters[:5]):
            with col:
                st.image(poster, use_container_width=True)
                st.caption(name)
        
        # 🔹 Second Row (5 Movies)
        cols2 = st.columns(5)
        for col, name, poster in zip(cols2, recommended_movie_names[5:], recommended_movie_posters[5:]):
            with col:
                st.image(poster, use_container_width=True)
                st.caption(name)
    else:
        st.warning("⚠️ No recommendations found. Try another movie!")

# Footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            text-align: center;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
    </style>
    <div class="footer">
        Developed by Hardik Chudasama 🚀
    </div>
""", unsafe_allow_html=True)
