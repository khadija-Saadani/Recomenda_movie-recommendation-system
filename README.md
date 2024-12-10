# Recomenda: Movie Recommendation System

## Overview
Recomenda is a machine learning-based movie recommendation system that helps users find movies similar to their favorite one. By inputting the title of their favorite movie, the system provides the top 30 closest matches, complete with titles, photos, and descriptions.

## Features
- **User Input**: Enter your favorite movie title.
- **Top 30 Recommendations**: Get a list of 30 movies that are most similar to your favorite movie.
- **Rich Movie Details**: Each recommended movie comes with its title, photo, and description.

## Technology Stack
- **Machine Learning Algorithms**:
  - **TF-IDF (Term Frequency-Inverse Document Frequency)**: Used for extracting and analyzing textual features.
  - **Cosine Similarity**: Computes the similarity between movies based on textual features.
- **Interface**: Built with **Streamlit** for an interactive and user-friendly experience.

## How It Works
1. The user inputs the title of their favorite movie.
2. The system computes similarity scores using the TF-IDF and Cosine Similarity algorithms.
3. The top 30 movies with the highest similarity scores are displayed to the user.
4. For each recommendation, the system shows:
   - The movie title
   - A photo of the movie
   - A brief description of the movie

## Contributions
Contributions are welcome! If you have ideas for improvements or encounter any issues, feel free to submit an issue or pull request.
