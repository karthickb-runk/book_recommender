from fastapi import FastAPI
from book_recommender.api import router

app = FastAPI(title="Book Recommendation API")
app.include_router(router)
