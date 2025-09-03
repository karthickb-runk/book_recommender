import streamlit as st
import pandas as pd
from book_recommender.config.env import DATA_PATH

books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")

def show_popular_books():
    st.header("📊 Popular Books Recommendation (Baseline)")

    tab1, tab2, tab3, tab4 = st.tabs(["⭐ By Rating", "📅 By Year", "🌍 By Language", "🔥 By Rating Count"])

    with tab1:
        st.subheader("⭐ Top 10 Books by Average Rating")
        popular_by_rating = books_clean.sort_values("average_rating", ascending=False).head(10)
        for i, (_, row) in enumerate(popular_by_rating.iterrows(), start=1):
            st.markdown(f"{i}. **{row['title']}** by {row['authors']} (⭐ {row['average_rating']})")

    with tab2:
        if "original_publication_year" in books_clean.columns:
            st.subheader("📅 Top 10 Recent Books")
            recent_books = (
                books_clean.dropna(subset=["original_publication_year"])
                .sort_values("original_publication_year", ascending=False)
                .head(10)
            )
            for i, (_, row) in enumerate(recent_books.iterrows(), start=1):
                st.markdown(
                    f"{i}. **{row['title']}** by {row['authors']} "
                    f"(📅 {int(row['original_publication_year'])}, ⭐ {row['average_rating']})"
                )
        else:
            st.warning("No year column found in dataset!")

    with tab3:
        if "language_code" in books_clean.columns:
            st.subheader("🌍 Popular Books by Language")
            selected_lang = st.selectbox(
                "Choose Language:", 
                options=sorted(books_clean["language_code"].dropna().unique())
            )
            lang_books = (
                books_clean[books_clean["language_code"] == selected_lang]
                .sort_values("average_rating", ascending=False)
                .head(10)
            )
            for i, (_, row) in enumerate(lang_books.iterrows(), start=1):
                st.markdown(
                    f"{i}. **{row['title']}** by {row['authors']} "
                    f"(Lang: {row['language_code']}, ⭐ {row['average_rating']})"
                )
        else:
            st.warning("No language column found in dataset!")

    with tab4:
        if "ratings_count" in books_clean.columns:
            st.subheader("🔥 Top 10 Books by Rating Count")
            popular_by_count = books_clean.sort_values("ratings_count", ascending=False).head(10)
            for i, (_, row) in enumerate(popular_by_count.iterrows(), start=1):
                st.markdown(
                    f"{i}. **{row['title']}** by {row['authors']} "
                    f"(💬 {row['ratings_count']} ratings, ⭐ {row['average_rating']})"
                )
        else:
            st.warning("No ratings_count column found in dataset!")

    st.markdown("---")