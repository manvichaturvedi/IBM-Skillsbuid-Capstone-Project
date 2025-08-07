import streamlit as st
import pickle 
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

import streamlit as st

footer_html = """
<div style='text-align: center;'>
    <p>Design & Developed by Manvi Chaturvedi</p>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

st.header("Movies Recommendation System Web App",divider='rainbow')
st.write("Author: Manvi Chaturvedi")
st.write("Technolgy: AI/ML")
st.write('Email: chatmanvi5@gmail.com')
st.markdown("""
<style>
   h1 {
      font-size: 25px;
      text-align: center;
      text-transform: uppercase;
   }
  [data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgb(15, 18, 23), rgb(44, 62, 80));
}

</style>
""", unsafe_allow_html=True)



def fetch_url(post_Link):
    url = "{}".format(post_Link)
    data = requests.get(url)
    path = data.content
    return path
#url = "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg"
#response = requests.get(url)
#img = Image.open(BytesIO(response.content))

movies = pickle.load(open("movies_list_new.pkl", 'rb'))
similarity = pickle.load(open("similarity_new.pkl", 'rb'))
movies_list = movies['Series_Title'].values

selected_movie = st.selectbox("select a movie :", movies_list)

import streamlit.components.v1 as components
index = pd.Series(movies['Series_Title'])
def movie_recommend(title):
    rec_movies = []
    movies_url = []
    idx = index[index == title].index[0]
    print(idx)
    score = pd.Series(similarity[idx]).sort_values(ascending = False)
    top10 = list(score.iloc[1:11].index)
    print(top10)
    
    for i in top10:
        rec_movies.append(movies['Series_Title'][i])
        movies_url.append(fetch_url(movies['Poster_Link'][i]))
    return rec_movies ,movies_url


if st.button("Show Recommendations"):
    movies_name, movie_poster = movie_recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(movies_name[0])
        st.image(movie_poster[0],width=150)
        st.write(movies_name[5])
        st.image(movie_poster[5],width=150)
    with col2:
        st.write(movies_name[1])
        st.image(movie_poster[1],width=150)
        st.write(movies_name[6])
        st.image(movie_poster[6],width=150)
    with col3:
        st.write(movies_name[2])
        st.image(movie_poster[2],width=150)
        st.write(movies_name[7])
        st.image(movie_poster[7],width=150)
    with col4:
        st.write(movies_name[3])
        st.image(movie_poster[3],width=150)
        st.write(movies_name[8])
        st.image(movie_poster[8],width=150)
    with col5:
        st.write(movies_name[4])
        st.image(movie_poster[4],width=150)
        st.write(movies_name[9])
        st.image(movie_poster[9],width=150)
       
    