import streamlit as st

from components import show_dataset_preview, show_popular_books, show_cbf_ui, show_cf_ui, show_hybrid_ui

st.set_page_config(page_title="Book Recommender", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📚 Book Recommendation System</h1>",
    unsafe_allow_html=True
)

show_dataset_preview()

show_popular_books()

show_cbf_ui()

show_cf_ui()

show_hybrid_ui()
