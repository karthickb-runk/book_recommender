import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from book_recommender.config.env import DATA_PATH

books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")
ratings_clean = pd.read_csv(f"{DATA_PATH}/ratings_clean.csv")

user_mapping = {u: i for i, u in enumerate(ratings_clean["user_id"].unique())}
book_mapping = {b: i for i, b in enumerate(ratings_clean["book_id"].unique())}

ratings_clean["user_idx"] = ratings_clean["user_id"].map(user_mapping)
ratings_clean["book_idx"] = ratings_clean["book_id"].map(book_mapping)

rating_matrix_sparse = csr_matrix(
    (ratings_clean["rating"], (ratings_clean["user_idx"], ratings_clean["book_idx"])),
    shape=(len(user_mapping), len(book_mapping))
)

user_similarity = cosine_similarity(rating_matrix_sparse, dense_output=False)
item_similarity = cosine_similarity(rating_matrix_sparse.T, dense_output=False)
