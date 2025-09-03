import numpy as np
import pandas as pd
from .utils import books_clean, book_mapping, item_similarity

def recommend_itemcf(book_id, top_n=10):
    if book_id not in book_mapping:
        return []

    book_idx = book_mapping[book_id]
    sim_scores = item_similarity[book_idx].toarray().ravel()
    sim_scores[book_idx] = 0

    similar_items_idx = np.argsort(-sim_scores)[:top_n]
    similar_books = [list(book_mapping.keys())[list(book_mapping.values()).index(i)] for i in similar_items_idx]

    result = books_clean[books_clean["book_id"].isin(similar_books)][
        ["book_id", "title", "authors", "average_rating"]
    ]
    result = result.merge(
        pd.DataFrame({"book_id": similar_books, "similarity": sim_scores[similar_items_idx]}),
        on="book_id"
    )
    return result.sort_values("similarity", ascending=False).to_dict(orient="records")
