import pandas as pd
from .cbf import recommend_cbf
from .usercf import recommend_usercf
from book_recommender.config.env import DATA_PATH

books_clean = pd.read_csv(f"{DATA_PATH}/books_clean.csv")

def recommend_hybrid(user_id: int, top_n: int = 10, alpha: float = 0.5):
    """
    Hybrid recommender = weighted combination of CBF + UserCF.
    alpha = weight for CBF
    """

    # Step 1: Get Collaborative Filtering recs
    cf_recs = recommend_usercf(user_id, top_n=top_n)
    if not cf_recs:
        return books_clean.sort_values("average_rating", ascending=False).head(top_n).to_dict(orient="records")

    # Step 2: Pick a top CF recommendation to use as a seed for CBF
    top_cf_book = cf_recs[0]["title"]
    cbf_recs = recommend_cbf(top_cf_book, top_n=top_n)

    # Convert to DataFrame
    cf_df = pd.DataFrame(cf_recs)
    cbf_df = pd.DataFrame(cbf_recs)

    # Assign scores
    cf_df["score_cf"] = range(len(cf_df), 0, -1)
    cbf_df["score_cbf"] = range(len(cbf_df), 0, -1)

    # Merge by book_id
    merged = pd.merge(cf_df, cbf_df, on="book_id", how="outer", suffixes=("_cf", "_cbf"))

    # Fill missing scores with 0
    merged["score_cf"].fillna(0, inplace=True)
    merged["score_cbf"].fillna(0, inplace=True)

    # Hybrid score
    merged["hybrid_score"] = alpha * merged["score_cbf"] + (1 - alpha) * merged["score_cf"]

    # Final ranking
    final = merged.sort_values("hybrid_score", ascending=False).head(top_n)

    return final[["book_id", "title_cf", "authors_cf", "average_rating_cf"]].rename(
        columns={
            "title_cf": "title",
            "authors_cf": "authors",
            "average_rating_cf": "average_rating"
        }
    ).to_dict(orient="records")
