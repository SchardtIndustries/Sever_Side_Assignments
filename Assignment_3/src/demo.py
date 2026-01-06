from pprint import pprint
from src.schema import ensure_indexes
from src.seed_books import seed_real_books
from src.crud import create_book, get_book_by_isbn, get_book_by_title, update_book, delete_book
from src.queries import (
    find_books_by_author, find_books_by_genre, find_books_published_between,
    top_10_highest_rated, find_books_with_magic_in_title
)
from src.aggregations import avg_pagecount_for_genre, author_with_most_books, avg_rating_after_year

def main():
    ensure_indexes()

    # Seed (idempotency not guaranteed because random titles; okay for assignment)
    print("Seeding 50 books...")
    try:
        # seed_real_books(50)
    except Exception as e:
        print("Seed warning (often duplicates on rerun):", e)

    # CRUD demo
    demo_isbn = "978-0-000000-0"
    demo_book = {
        "title": "Magic in the Server Room",
        "authors": ["J.K. Rowling"],
        "isbn": demo_isbn,
        "publicationYear": 2012,
        "genres": ["Fantasy"],
        "description": "A magical tale of debugging and databases.",
        "pageCount": 333,
        "averageRating": 4.7,
        "numberOfRatings": 900
    }

    print("\nCREATE:")
    try:
        create_book(demo_book)
        print("Created:", demo_isbn)
    except Exception as e:
        print("Create warning (maybe already exists):", e)

    print("\nREAD by ISBN:")
    pprint(get_book_by_isbn(demo_isbn))

    print("\nREAD by Title:")
    pprint(get_book_by_title("Magic in the Server Room"))

    print("\nUPDATE:")
    print("Modified:", update_book(demo_isbn, {"pageCount": 350, "averageRating": 4.8}))

    print("\nDELETE:")
    print("Deleted:", delete_book(demo_isbn))

    # Phase 4 queries
    print("\nQUERY: books by J.K. Rowling:")
    print(len(find_books_by_author("J.K. Rowling")))

    print("\nQUERY: Science Fiction books:")
    print(len(find_books_by_genre("Science Fiction")))

    print("\nQUERY: books published 1990-2000:")
    print(len(find_books_published_between(1990, 2000)))

    print("\nQUERY: top 10 highest rated:")
    pprint(top_10_highest_rated())

    print("\nQUERY: books with 'Magic' in title:")
    pprint(find_books_with_magic_in_title()[:5])

    # Phase 5 aggregations
    print("\nAGG: avg pageCount for Fantasy:")
    pprint(avg_pagecount_for_genre("Fantasy"))

    print("\nAGG: author with most books:")
    pprint(author_with_most_books())

    print("\nAGG: avg rating after 2010:")
    pprint(avg_rating_after_year(2010))

if __name__ == "__main__":
    main()
