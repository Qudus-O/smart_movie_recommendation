
import streamlit as st
import pandas as pd
import numpy as np
import difflib
import requests
import pickle
from dotenv import load_dotenv  
import os


st.set_page_config(page_title="Movie Recommendation System", layout="wide")
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")


with open('smart_movies_recommendation.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file) 



def get_smart_recommendation(title, genre=None, movies_df=movies, cosine_sim=cosine_sim):
    title_clean = title.strip()
    all_titles = movies_df['title'].tolist()

    # Scenario A: Exact match found
    if title_clean in all_titles:
        target_title = title_clean
    else:
    # Scenario B: Exact match fails, check for fuzzy string matching 
        matches = difflib.get_close_matches(title_clean, all_titles, n=1, cutoff=0.6)
        if matches:
            target_title = matches[0]
            st.info(f"💡 '{title_clean}' not found. Did you mean **{target_title}**?")
        else:
            # Scenario C: Look for the fallback genre option if provided
            if genre and genre != "None":
                genre_matches = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
                if not genre_matches.empty:
                    st.warning(f" '{title_clean}' not found. Displaying popular '{genre}' movies instead:")
                    return genre_matches['title'].head(10).reset_index(drop=True)
            
            # Scenario D: Deep fallback check - see if the text inside 'title' was actually meant to be a genre
            fallback_genre = movies_df[movies_df['genres'].str.contains(title_clean, case=False, na=False)]

            if not fallback_genre.empty:
                st.warning(f"⚠️ '{title_clean}' not found as a title, but matching the genre instead:")
                return fallback_genre['title'].head(10).reset_index(drop=True)

            return "Could not find any matching movies or genres. Please check your spelling!"

    # Compute indices from the target title row inside the similarity matrix
    idx = movies_df[movies_df['title'] == target_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores[1:11]]

    # Returns a Pandas Series containing only the matching text strings
    return movies_df['title'].iloc[movie_indices].reset_index(drop=True)


#  FETCHING API 
def get_movie_poster(movie_title):
    """Fetches high resolution poster paths via TMDB search API using string strings."""
    if not api_key:
        return "https://via.placeholder.com/500x750?text=No+API+Key"
        
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    try:
        response = requests.get(search_url, timeout=5)
        data = response.json()
        if data.get('results') and data['results'][0].get('poster_path'):
            poster_path = data['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=Poster+Not+Found"


# FRONTEND
st.title(" Smart Movies Recommendation System")
st.markdown("Discover movies based on title and genre.")
st.hr()

# Multi-column input layout for the user actions
col_input1, col_input2 = st.columns([2, 1])

with col_input1:
    # FIX 1: Added placeholder text to guide users on the expected input format
    user_movie_input = st.text_input("Enter a movie title (Compulsory):", placeholder="e.g., Toy Story, Mortal Kombat..")

with col_input2:
    # Optional dropdown fallback for genres extraction
    genre_options = ["None", "Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Horror", "Romance", "Adventure"]
    selected_genre = st.selectbox("Select fallback genre (Optional):", options=genre_options)

st.write("") # Extra spacing spacer


if st.button("Generate Recommendations", type="primary"):
    if not user_movie_input.strip():
        st.error("Please enter a valid movie title to begin searching.")
    else:
        with st.spinner("Processing metadata correlations..."):
            recommendations = get_smart_recommendation(user_movie_input, genre=selected_genre)
            
        # Verify if recommendations returned a valid Pandas Series object or a string error message
        if isinstance(recommendations, str):
            st.error(recommendations)
        else:
            st.subheader("Handpicked Recommendations For You:")
            
            # Grid construction: Displays 10 results neatly split across two rows of 5 columns
            for i in range(0, 10, 5):
                cols = st.columns(5)
                for col, j in zip(cols, range(i, i+5)):
                    if j < len(recommendations):
                        
                        recommended_title = recommendations.iloc[j]
                        poster_url = get_movie_poster(recommended_title)
                        
                        with col:
                            
                            st.image(poster_url, use_container_width=True)
                            st.markdown(f"**{recommended_title}**")
