from .db import get_db

def avg_pagecount_for_genre(genre: str):
    db = get_db()
    pipeline = [
        {"$match": {"genres": genre}},
        {"$group": {"_id": genre, "avgPages": {"$avg": "$pageCount"}, "count": {"$sum": 1}}},
    ]
    return list(db.books.aggregate(pipeline))

def author_with_most_books():
    db = get_db()
    pipeline = [
        {"$unwind": "$authors"},
        {"$group": {"_id": "$authors", "bookCount": {"$sum": 1}}},
        {"$sort": {"bookCount": -1}},
        {"$limit": 1},
    ]
    return list(db.books.aggregate(pipeline))

def avg_rating_after_year(year: int):
    db = get_db()
    pipeline = [
        {"$match": {"publicationYear": {"$gt": year}}},
        {"$group": {"_id": f"after_{year}", "avgRating": {"$avg": "$averageRating"}, "count": {"$sum": 1}}},
    ]
    return list(db.books.aggregate(pipeline))
