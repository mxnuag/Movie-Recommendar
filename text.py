import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id): 
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=15a72db1be97275cbf691a462784938a&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path'] 

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    movie_names = [] 
    movie_posters = [] 

    for i in similar_movies:
        movie_names.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        movie_posters.append(fetch_poster(movie_id))

    return movie_names, movie_posters

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Custom CSS to change background color
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select Movie of your choice ',
                                   movies['title'].values)

if st.button('Recommend Similar Movies'):
    names, posters = recommend(selected_movie_name)
    movie1, movie2, movie3, movie4, movie5 = st.columns(5) 
    with movie1:
        st.text(names[0])
        st.image(posters[0])
    with movie2:
        st.text(names[1])
        st.image(posters[1])
    with movie3:
        st.text(names[2])
        st.image(posters[2])
    with movie4:
        st.text(names[3])
        st.image(posters[3])
    with movie5:
        st.text(names[4])
        st.image(posters[4])
