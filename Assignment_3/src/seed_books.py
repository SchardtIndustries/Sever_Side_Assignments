import os
import re
import time
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from pymongo.errors import BulkWriteError

from .db import get_db
from .schema import ensure_indexes

AUTHORS = [
    "J.K. Rowling", "George R.R. Martin", "Brandon Sanderson", "Ursula K. Le Guin",
    "Isaac Asimov", "Frank Herbert", "Agatha Christie", "Stephen King",
    "Neil Gaiman", "Terry Pratchett", "Octavia E. Butler", "Arthur C. Clarke",
    "Suzanne Collins", "Haruki Murakami", "Margaret Atwood", "J.R.R. Tolkien"
]

GENRE_MAP = [
    # crude mapping from OpenLibrary "subject" text -> your genres
    (re.compile(r"fantasy", re.I), "Fantasy"),
    (re.compile(r"science fiction|sci[- ]?fi", re.I), "Science Fiction"),
    (re.compile(r"mystery|detective|crime", re.I), "Mystery"),
    (re.compile(r"thriller|suspense", re.I), "Thriller"),
    (re.compile(r"horror", re.I), "Horror"),
    (re.compile(r"romance", re.I), "Romance"),
    (re.compile(r"history|historical", re.I), "Historical"),
    (re.compile(r"nonfiction|biography|memoir|essay", re.I), "Nonfiction"),
    (re.compile(r"adventure", re.I), "Adventure"),
    (re.compile(r"drama", re.I), "Drama"),
]

def map_subjects_to_genres(subjects: List[str]) -> List[str]:
    found: Set[str] = set()
    for s in subjects:
        for rx, g in GENRE_MAP:
            if rx.search(s):
                found.add(g)
    # keep it reasonable
    if not found:
        return []
    return sorted(found)[:3]

def choose_isbn(doc: Dict[str, Any]) -> Optional[str]:
    """
    Prefer ISBN-13 if available. OpenLibrary may return:
      - isbn: [ ... ]
    We’ll pick the first 13-digit, else first 10-digit.
    """
    isbns = doc.get("isbn") or []
    if not isbns:
        return None
    for x in isbns:
        digits = re.sub(r"[^0-9Xx]", "", x)
        if len(digits) == 13 and digits.isdigit():
            return digits
    for x in isbns:
        digits = re.sub(r"[^0-9Xx]", "", x)
        if len(digits) == 10:
            return digits.upper()
    return None

def ol_search_author(author: str, limit: int = 50, page: int = 1) -> Dict[str, Any]:
    # Open Library Search API
    url = "https://openlibrary.org/search.json"
    params = {
        "author": author,
        "limit": limit,
        "page": page,
        # ask for useful fields
        "fields": "title,author_name,first_publish_year,isbn,subject,number_of_pages_median",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def build_book_doc(raw: Dict[str, Any], fallback_author: str) -> Optional[Dict[str, Any]]:
    title = raw.get("title")
    if not title:
        return None

    authors = raw.get("author_name") or [fallback_author]
    isbn = choose_isbn(raw)
    if not isbn:
        return None  # we need an ISBN for your assignment + lookups

    pub_year = raw.get("first_publish_year")
    if not isinstance(pub_year, int):
        pub_year = None

    subjects = raw.get("subject") or []
    genres = map_subjects_to_genres(subjects)
    # Guarantee at least one genre for Phase 4 queries:
    if not genres and subjects:
        genres = [subjects[0][:40]]
    if not genres:
        genres = ["Drama"]  # safe fallback from your allowed list? (your allowed list isn't enforced in Mongo)

    page_count = raw.get("number_of_pages_median")
    if not isinstance(page_count, int):
        page_count = random.randint(120, 900)

    # OpenLibrary doesn’t provide ratings in search results.
    # We’ll generate rating fields so your Phase 4/5 tasks work.
    avg_rating = round(random.uniform(3.2, 4.9), 2)
    num_ratings = random.randint(10, 5000)

    now = datetime.now(timezone.utc)
    return {
        "title": title,
        "authors": authors,
        "isbn": isbn,
        "publicationYear": pub_year if pub_year is not None else random.randint(1950, 2024),
        "genres": genres,
        "description": f"Imported from Open Library for author seed '{fallback_author}'.",
        "pageCount": page_count,
        "averageRating": avg_rating,
        "numberOfRatings": num_ratings,
        "createdAt": now,
        "updatedAt": now,
        "source": {
            "provider": "openlibrary",
        },
    }

def seed_real_books(target_count: int = 50, per_author_pages: int = 3, sleep_s: float = 0.25) -> int:
    """
    Pull books for AUTHORS from OpenLibrary until we have target_count unique ISBNs.
    """
    db = get_db()
    ensure_indexes()
    books = db.books

    collected: List[Dict[str, Any]] = []
    seen_isbn: Set[str] = set()

    # Prefer spreading across authors
    for author in AUTHORS:
        for page in range(1, per_author_pages + 1):
            data = ol_search_author(author, limit=50, page=page)
            docs = data.get("docs") or []
            for raw in docs:
                doc = build_book_doc(raw, fallback_author=author)
                if not doc:
                    continue
                if doc["isbn"] in seen_isbn:
                    continue
                seen_isbn.add(doc["isbn"])
                collected.append(doc)
                if len(collected) >= target_count:
                    break
            if len(collected) >= target_count:
                break
            time.sleep(sleep_s)
        if len(collected) >= target_count:
            break

    if len(collected) < target_count:
        raise RuntimeError(f"Only collected {len(collected)} books with ISBNs. Increase per_author_pages or target_count.")

    # Insert; ignore duplicates if you rerun (because isbn_unique)
    try:
        result = books.insert_many(collected, ordered=False)
        return len(result.inserted_ids)
    except BulkWriteError as e:
        # duplicates on rerun; count inserted
        inserted = e.details.get("nInserted", 0)
        return inserted

if __name__ == "__main__":
    inserted = seed_real_books(target_count=50)
    print(f"Inserted {inserted} real books (Open Library) into book_catalog.books")
