import streamlit as st
import pandas as pd
import requests
from book_recommender.config.env import API_URL, DATA_PATH

books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")

def show_cbf_ui():
    st.header("Content-Based Filtering (CBF)")
    book_name = st.selectbox("Select a book:", options=books_clean["title"].dropna().unique())
    if st.button("Get CBF Recommendations"):
        response = requests.get(f"{API_URL}/recommend/cbf", params={"title": book_name})
        data = response.json()
        if data.get("recommendations"):
            for i, rec in enumerate(data["recommendations"], start=1):
                st.markdown(f"{i}. **{rec['title']}** by {rec['authors']} (⭐ {rec['average_rating']})")
        else:
            st.warning("No recommendations found.")
    st.markdown("---")