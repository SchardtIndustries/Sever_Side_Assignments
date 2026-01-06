from pymongo import ASCENDING, DESCENDING, TEXT
from .db import get_db

def ensure_indexes():
    db = get_db()
    books = db.books

    # Unique ISBN
    books.create_index([("isbn", ASCENDING)], unique=True, name="isbn_unique")

    # Multi-key indexes for arrays
    books.create_index([("authors", ASCENDING)], name="authors_idx")
    books.create_index([("genres", ASCENDING)], name="genres_idx")

    # Range queries by year
    books.create_index([("publicationYear", ASCENDING)], name="pubyear_idx")

    # Sorting by rating (top 10)
    books.create_index([("averageRating", DESCENDING)], name="rating_desc_idx")

    # Title search: use text index for "Magic"
    books.create_index([("title", TEXT)], name="title_text_idx")
