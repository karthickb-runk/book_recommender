import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

from book_recommender.config.env import DATA_PATH

# Load dataset
books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")

# ----- Build features once on startup -----
# Title → TF-IDF
tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
X_title = tfidf.fit_transform(books_clean["title"].fillna(""))

# Author → OneHot
ohe = OneHotEncoder(sparse_output=True, handle_unknown="ignore")
X_author = ohe.fit_transform(books_clean[["authors"]])

# Language → OneHot
X_lang = pd.get_dummies(books_clean["language_code"], prefix="lang").values

# Numerical features → scaled
scaler = MinMaxScaler()
X_num = scaler.fit_transform(
    books_clean[["average_rating", "ratings_count", "original_publication_year"]].fillna(0)
)

# Combine all features
X_features = sp.hstack([X_title, X_author, X_lang, X_num])

# Precompute similarity (kept in memory)
cosine_sim = cosine_similarity(X_features, X_features)

# ----- Recommender function -----
def recommend_cbf(title: str, top_n: int = 10):
    # Find book index
    matches = books_clean[books_clean["title"].str.lower() == title.lower()]
    if matches.empty:
        return []
    
    idx = matches.index[0]

    # Similarity scores for this book
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    # Get top N book indices
    book_indices = [i[0] for i in sim_scores]

    return books_clean.iloc[book_indices][
        ["book_id", "title", "authors", "average_rating"]
    ].to_dict(orient="records")
