# ui/hybrid_ui.py
import streamlit as st
import pandas as pd
import requests
from book_recommender.config.env import API_URL, DATA_PATH

ratings_clean = pd.read_csv(f"{DATA_PATH}/ratings_clean.csv")


def show_hybrid_ui():
    st.header("Hybrid Recommendations")

    hybrid_user = st.selectbox(
        "Select User ID:",
        options=sorted(ratings_clean["user_id"].dropna().unique()),
        key="user_hybrid"
    )

    if st.button("Get Hybrid Recommendations"):
        try:
            response = requests.get(f"{API_URL}/recommend/hybrid/{hybrid_user}")
            data = response.json()

            if data.get("recommendations"):
                for i, rec in enumerate(data["recommendations"], start=1):
                    st.markdown(
                        f"{i}. **{rec['title']}** by {rec['authors']} "
                        f"(⭐ {rec['average_rating']:.2f})"
                    )
            else:
                st.warning("No hybrid recommendations found.")
        except Exception as e:
            st.error(f"Failed to fetch recommendations: {str(e)}")
