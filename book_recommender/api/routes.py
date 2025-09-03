from fastapi import APIRouter
from .recommender import recommend_cbf, recommend_usercf, recommend_itemcf, recommend_hybrid

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True}

@router.get("/recommend/cbf")
def recommend_cbf_api(title: str):
    try:
        return {"recommendations": recommend_cbf(title)}
    except:
        return {"error": "Book not found"}

@router.get("/recommend/usercf/{user_id}")
def recommend_usercf_api(user_id: int):
    return {"recommendations": recommend_usercf(user_id)}

@router.get("/recommend/itemcf/{book_id}")
def recommend_itemcf_api(book_id: int):
    return {"recommendations": recommend_itemcf(book_id)}

@router.get("/recommend/hybrid/{user_id}")
def recommend_hybrid_api(user_id: int, alpha: float = 0.5):
    return {"recommendations": recommend_hybrid(user_id, alpha=alpha)}