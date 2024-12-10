import streamlit as st
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import time  # Pour gérer la pause

# Charger les datasets
@st.cache_data
def load_data():
    movies_data = pd.read_csv('movies.csv')
    genre_data = pd.read_csv('MovieGenre.csv', encoding='latin1')
    movies_data = movies_data.fillna('')
    genre_data = genre_data.fillna('')
    return movies_data, genre_data

movies_data, genre_data = load_data()

# Normaliser les titres pour une correspondance robuste
movies_data['normalized_title'] = movies_data['title'].str.lower().str.strip()
genre_data['normalized_title'] = genre_data['Title'].str.lower().str.strip()

# Préparer les fonctionnalités combinées pour le premier dataset
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
movies_data['combined_features'] = movies_data[selected_features].apply(lambda x: ' '.join(x), axis=1)

# Vectorisation TF-IDF et calcul de similarité cosinus
@st.cache_data
def compute_similarity(data):
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(data['combined_features'])
    similarity = cosine_similarity(feature_vectors)
    return similarity

similarity = compute_similarity(movies_data)

# Initialisation de l'état de la session
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_movie_index" not in st.session_state:
    st.session_state.selected_movie_index = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "loading_done" not in st.session_state:
    st.session_state.loading_done = False

# Fonction pour afficher le logo circulaire en haut à gauche
def display_logo(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .logo-container {{
            position: absolute;
            top: 5px; /* Position verticale */
            left: 10px; /* Position horizontale */
            width: 60px;
            height: 60px;
            border-radius: 50%;
            overflow: hidden;
            z-index: 1000;
        }}
        .logo-container img {{
            width: 100%;
            height: auto;
        }}
        .main-title {{
            margin-top: 80px; /* Espace sous le logo */
        }}
        </style>
        <div class="logo-container">
            <img src="data:image/png;base64,{encoded_image}" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Phase de chargement
if not st.session_state.loading_done:
    with st.empty():
        st.markdown(
            """
            <style>
            @keyframes smooth-blink {
                0% { color: red; opacity: 0.7; }
                50% { color: black; opacity: 1; }
                100% { color: red; opacity: 0.7; }
            }
            .blinking-text {
                font-size: 32px;
                font-weight: bold;
                animation: smooth-blink 2s infinite ease-in-out;
                text-align: center;
                margin-top: 40%;
            }
            </style>
            <div class="blinking-text">Le cinéma inspire, Recomenda guide.</div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(2)  # Pause de 2 secondes
    st.session_state.loading_done = True
    st.experimental_rerun()

# Page principale
if st.session_state.page == "home":
    logo_path = "movo.JPG"  # Assurez-vous que le fichier existe dans le dossier
    display_logo(logo_path)
    st.markdown('<h1 class="main-title">Système de Recommandation de Films</h1>', unsafe_allow_html=True)
    st.subheader("Trouvez des films similaires à vos favoris 🎥")

    # Entrée utilisateur
    movie_name = st.text_input("Entrez le nom de votre film préféré :")

    # Afficher les recommandations
    if st.button("Afficher les films recommandés"):
        if movie_name:
            list_of_all_titles = movies_data['title'].tolist()
            find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

            if find_close_match:
                close_match = find_close_match[0]
                st.write(f"Film trouvé : **{close_match}**")

                index_of_the_movie = movies_data[movies_data.title == close_match].index[0]
                similarity_score = list(enumerate(similarity[index_of_the_movie]))
                sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
                st.session_state.recommendations = sorted_similar_movies[1:21]
            else:
                st.write("Désolé, aucun film correspondant trouvé.")
        else:
            st.write("Veuillez entrer le nom d'un film pour afficher des recommandations.")

    if st.session_state.recommendations:
        st.subheader("Films suggérés pour vous :")
        columns = st.columns(4)
        for i, movie in enumerate(st.session_state.recommendations):
            index = movie[0]
            title_from_index = movies_data.loc[index, 'title']

            normalized_title = title_from_index.lower().strip()
            poster_url = None

            poster_match = genre_data.loc[genre_data['normalized_title'] == normalized_title, 'Poster'].values
            if poster_match.size > 0:
                poster_url = poster_match[0]
            else:
                close_titles = difflib.get_close_matches(normalized_title, genre_data['normalized_title'].tolist(), n=1, cutoff=0.8)
                if close_titles:
                    poster_match = genre_data.loc[genre_data['normalized_title'] == close_titles[0], 'Poster'].values
                    if poster_match.size > 0:
                        poster_url = poster_match[0]

            poster_url = poster_url if poster_url else 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

            col = columns[i % 4]
            with col:
                st.image(poster_url, width=150)
                if st.button(f"{title_from_index}", key=f"button_{index}"):
                    st.session_state.page = "details"
                    st.session_state.selected_movie_index = index
                    st.experimental_rerun()

# Page des détails
elif st.session_state.page == "details":
    selected_index = st.session_state.selected_movie_index
    if selected_index is not None:
        selected_movie = movies_data.loc[selected_index]

        normalized_title = selected_movie['title'].lower().strip()
        poster_url = None
        poster_match = genre_data.loc[genre_data['normalized_title'] == normalized_title, 'Poster'].values
        if poster_match.size > 0:
            poster_url = poster_match[0]
        else:
            close_titles = difflib.get_close_matches(normalized_title, genre_data['normalized_title'].tolist(), n=1, cutoff=0.8)
            if close_titles:
                poster_match = genre_data.loc[genre_data['normalized_title'] == close_titles[0], 'Poster'].values
                if poster_match.size > 0:
                    poster_url = poster_match[0]

        poster_url = poster_url if poster_url else 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

        st.image(poster_url, width=300)
        st.markdown(f"### {selected_movie['title']}")
        st.markdown(f"**Description :** {selected_movie['overview']}")

        if st.button("Retour"):
            st.session_state.page = "home"
            st.experimental_rerun()
    else:
        st.write("Aucun film sélectionné.") 