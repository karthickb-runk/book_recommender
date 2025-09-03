from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from book_recommender.api import router

origins = ["*"]

app = FastAPI(title="Book Recommendation API")
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)