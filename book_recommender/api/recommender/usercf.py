import numpy as np
from .utils import ratings_clean, books_clean, user_mapping, user_similarity

def recommend_usercf(user_id, top_n=10):
    if user_id not in user_mapping:
        return []

    user_idx = user_mapping[user_id]
    sim_scores = user_similarity[user_idx].toarray().ravel()
    sim_scores[user_idx] = 0

    similar_users = np.argsort(-sim_scores)
    rated_books = ratings_clean[ratings_clean["user_id"] == user_id]["book_id"].tolist()
    scores = {}

    for neighbor_idx in similar_users:
        similarity = sim_scores[neighbor_idx]
        if similarity <= 0:
            continue

        neighbor_id = list(user_mapping.keys())[list(user_mapping.values()).index(neighbor_idx)]
        neighbor_ratings = ratings_clean[ratings_clean["user_id"] == neighbor_id]

        for _, row in neighbor_ratings.iterrows():
            book = row["book_id"]
            rating = row["rating"]
            if book not in rated_books:
                scores[book] = scores.get(book, 0) + similarity * rating

    recommended_books = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return books_clean[books_clean["book_id"].isin([b for b, _ in recommended_books])][
        ["book_id", "title", "authors", "average_rating"]
    ].to_dict(orient="records")
