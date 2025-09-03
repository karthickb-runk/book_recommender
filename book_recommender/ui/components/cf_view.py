import streamlit as st
import pandas as pd
import requests
from book_recommender.config.env import API_URL, DATA_PATH

books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")
ratings_clean = pd.read_csv(f"{DATA_PATH}/ratings_clean.csv")

def show_cf_ui():
    st.header("Collaborative Filtering (UserCF & ItemCF)")
    tab1, tab2 = st.tabs(["UserCF", "ItemCF"])

    with tab1:
        user_id = st.selectbox(
            "Select User ID:",
            options=ratings_clean["user_id"].dropna().unique(),
            key="user_cf"
        )
        if st.button("Get UserCF Recommendations"):
            response = requests.get(f"{API_URL}/recommend/usercf/{user_id}")
            data = response.json()
            if data.get("recommendations"):
                for i, rec in enumerate(data["recommendations"], start=1):
                    st.markdown(f"{i}. **{rec['title']}** by {rec['authors']} (⭐ {rec['average_rating']})")
            else:
                st.warning("No recommendations found.")

    with tab2:
        valid_book_ids = ratings_clean["book_id"].unique()
        valid_book_ids = [b for b in valid_book_ids if b in books_clean["book_id"].values]
        book_id = st.selectbox("Select Book ID:", options=valid_book_ids)
        if st.button("Get ItemCF Recommendations"):
            response = requests.get(f"{API_URL}/recommend/itemcf/{book_id}")
            data = response.json()
            if data.get("recommendations"):
                for i, rec in enumerate(data["recommendations"], start=1):
                    st.markdown(f"{i}. **{rec['title']}** by {rec['authors']} (⭐ {rec['average_rating']}) | Similarity: {round(rec['similarity'], 3)}")
            else:
                st.warning("No recommendations found.")

    st.markdown("---")