from .db import get_db

def find_books_by_author(author: str):
    db = get_db()
    return list(db.books.find({"authors": author}))

def find_books_by_genre(genre: str):
    db = get_db()
    return list(db.books.find({"genres": genre}))

def find_books_published_between(start_year: int, end_year: int):
    db = get_db()
    return list(db.books.find({"publicationYear": {"$gte": start_year, "$lte": end_year}}))

def top_10_highest_rated():
    db = get_db()
    return list(db.books.find({}, {"title": 1, "averageRating": 1, "authors": 1}).sort("averageRating", -1).limit(10))

def find_books_with_magic_in_title():
    db = get_db()
    # Uses text index on title
    return list(db.books.find({"$text": {"$search": "Magic"}}, {"score": {"$meta": "textScore"}, "title": 1, "authors": 1})
                .sort([("score", {"$meta": "textScore"})]))
