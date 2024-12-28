import pickle
import streamlit as st
import requests
import os

# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6de40a58f8ef00a3ca70dcd3f443c01d"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', "")
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    return full_path

# Function to reassemble the similarity matrix from chunks
def load_similarity_from_chunks(chunk_dir):
    chunk_files = sorted(os.listdir(chunk_dir), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    similarity = []
    for chunk_file in chunk_files:
        with open(os.path.join(chunk_dir, chunk_file), 'rb') as file:
            similarity.extend(pickle.load(file))
    return similarity

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit App
st.header('Movie Recommender System')

# Load movies dataset
movies = pickle.load(open('movies.pkl', 'rb'))

# Load similarity matrix from chunks
chunk_dir = "similarity_chunks"
if os.path.exists(chunk_dir):
    similarity = load_similarity_from_chunks(chunk_dir)
else:
    st.error("Chunks directory not found. Please ensure the 'similarity_chunks' folder exists.")

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Recommend movies on button click
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[i])
            st.text(recommended_movie_names[i])
