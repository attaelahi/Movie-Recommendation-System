import streamlit as st
import pandas as pd

# Load CSS styles
css_styles = """
<style>
    h1 {
        font-family: "Arial", sans-serif;
        color: #333333;
        text-align: center;
    }
    
    .stMultiSelect, .stSelectbox {
        font-size: 16px;
        color: #555555;
    }
    
    .stTextArea {
        font-size: 14px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #cccccc;
    }
    
    .stButton {
        font-size: 16px;
        padding: 10px 20px;
        background-color: #007bff;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .recommendation {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# Load movie data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')
movie_data = pd.merge(movies, ratings, on='movieId', how='left')

# Define genres and rating options
genres = movie_data['genres'].unique()
rating_values = movie_data['rating'].unique()

# Create user preference inputs
st.title('Movie Recommendation System')
selected_genres = st.multiselect('Select Genres', genres)
min_rating = st.selectbox('Minimum Rating', rating_values)
browsing_history = st.text_area('Enter your browsing history (movie titles separated by commas):')
browsed_movies = [movie.strip() for movie in browsing_history.split(',')]

# Recommendation button
if st.button('Recommend'):
    # Filter movies based on user preferences
    if selected_genres and min_rating:
        filtered_movies = movie_data[(movie_data['genres'].isin(selected_genres)) & (movie_data['rating'] >= min_rating)]
    else:
        filtered_movies = movie_data.copy()

    # Filter movies based on browsing history
    if browsed_movies:
        filtered_movies = filtered_movies[~filtered_movies['title'].isin(browsed_movies)]

    # Display recommendations
    if filtered_movies.empty:
        st.write('No recommendations found based on your preferences.')
    else:
        st.write('Recommendations:')
        for _, row in filtered_movies.iterrows():
            st.markdown(f"""
                <div class="recommendation">
                    <h3>{row['title']} ({row['timestamp']})</h3>
                    <p>Genres: {row['genres']}</p>
                    <p>Rating: {row['rating']}</p>
                </div>
            """, unsafe_allow_html=True)