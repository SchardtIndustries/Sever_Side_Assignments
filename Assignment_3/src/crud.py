from datetime import datetime, timezone
from .db import get_db

def create_book(book_data: dict):
    db = get_db()
    now = datetime.now(timezone.utc)
    book_data.setdefault("createdAt", now)
    book_data["updatedAt"] = now
    return db.books.insert_one(book_data).inserted_id

def get_book_by_isbn(isbn: str):
    db = get_db()
    return db.books.find_one({"isbn": isbn})

def get_book_by_title(title: str):
    db = get_db()
    return db.books.find_one({"title": title})

def update_book(isbn: str, updates: dict):
    db = get_db()
    updates["updatedAt"] = datetime.now(timezone.utc)
    result = db.books.update_one({"isbn": isbn}, {"$set": updates})
    return result.modified_count

def delete_book(isbn: str):
    db = get_db()
    result = db.books.delete_one({"isbn": isbn})
    return result.deleted_count
