# 📚 Book Recommender System

### A hybrid Book Recommendation System built with FastAPI (backend) and Streamlit (frontend). It supports multiple recommendation strategies:

- Content-Based Filtering (CBF)
- Collaborative Filtering (User & Item based)
- Hybrid Model (combining CBF & CF)
- Popular books by rating

# 📂 Project Structure

```
book_recommender/
│── book_recommender/
│   ├── api/              # FastAPI backend (recommendation APIs)
│   ├── ui/               # Streamlit frontend (user interface)
│   ├── config/           # Environment variables & config
│   ├── data/             # CSV datasets (clean & raw)
│   ├── models/           # Pickle files (CBF vectorizer, etc.)
│   └── __init__.py
│
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignore unnecessary files
├── .env                  # Environment variables (API_URL, DATA_PATH, etc.)
└── README.md
```

## ⚙️ Installation

```bash
# Clone repo
git clone https://github.com/your-username/book_recommender.git
cd book_recommender

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Copy the example file and Update .env with your values
cp env.example .env

# Install dependencies
pip install -r requirements.txt
```

# 🚀 Run the Project

```
uvicorn book_recommender.api.main:app --reload

PYTHONPATH=. streamlit run book_recommender/ui/main.py
```

# 📊 Datasets

- **books.csv / ratings.csv** → raw data
- **books_clean.csv / ratings_clean.csv** → preprocessed data (used in app)