from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import pandas as pd
import scipy.sparse as sp

from book_recommender.config.env import DATA_PATH

books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")

def build_features():
    tfidf = TfidfVectorizer(stop_words="english", max_features=2000)
    X_title = tfidf.fit_transform(books_clean["title"].fillna(""))

    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_author = ohe.fit_transform(books_clean[["authors"]])

    X_lang = pd.get_dummies(books_clean["language_code"], prefix="lang").values

    scaler = MinMaxScaler()
    X_num = scaler.fit_transform(
        books_clean[["average_rating", "ratings_count", "original_publication_year"]].fillna(0)
    )

    return sp.hstack([X_title, X_author, X_lang, X_num])

def recommend_cbf(title, top_n=10):
    matches = books_clean[books_clean["title"].str.lower() == title.lower()]
    if matches.empty:
        return []

    X_features = build_features()
    cosine_sim = cosine_similarity(X_features, X_features)
    idx = matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    book_indices = [i[0] for i in sim_scores]
    return books_clean.iloc[book_indices][["book_id", "title", "authors", "average_rating"]].to_dict(orient="records")
