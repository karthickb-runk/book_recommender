import streamlit as st
import pandas as pd

from book_recommender.config.env import DATA_PATH

books_original = pd.read_csv(f"{DATA_PATH}/books.csv")
books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")
ratings_original = pd.read_csv(f"{DATA_PATH}/ratings.csv")
ratings_clean = pd.read_csv(f"{DATA_PATH}/ratings_clean.csv")

def show_dataset_preview():
    st.header("Datasets Preview")

    tab1, tab2 = st.tabs(["📄 Original Dataset", "🧹 Cleaned Dataset"])

    with tab1:
        st.subheader("Original Books Dataset")
        st.dataframe(books_original)
        st.caption(f"Shape: {books_original.shape[0]} rows × {books_original.shape[1]} columns")

        st.subheader("Original Ratings Dataset")
        st.dataframe(ratings_original)
        st.caption(f"Shape: {ratings_original.shape[0]} rows × {ratings_original.shape[1]} columns")

    with tab2:
        st.subheader("Cleaned Books Dataset")
        st.dataframe(books_clean)
        st.caption(f"Shape: {books_clean.shape[0]} rows × {books_clean.shape[1]} columns")

        st.subheader("Cleaned Ratings Dataset")
        st.dataframe(ratings_clean)
        st.caption(f"Shape: {ratings_clean.shape[0]} rows × {ratings_clean.shape[1]} columns")

    st.markdown("---")