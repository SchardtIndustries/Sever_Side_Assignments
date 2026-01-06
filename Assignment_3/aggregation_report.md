Aggregation Results and Analysis

1. Average Page Count for Fantasy Books

The aggregation calculated the average page count for books in the Fantasy genre.
The result shows an average length of approximately 760 pages across 23 fantasy books in the dataset. This indicates that fantasy titles in the catalog tend to be longer, which is consistent with the genre’s emphasis on detailed world-building and complex narratives.

2. Author with the Most Books

The aggregation identified J.K. Rowling as the author with the highest number of books in the database, totaling 42 books. This result reflects the dataset’s focus on popular and prolific authors and demonstrates the effectiveness of using $unwind and $group stages to analyze array-based fields such as authors.

3. Average Rating for Books Published After 2010

The final aggregation calculated the average rating for books published after the year 2010. The result shows an average rating of approximately 4.09 across 19 books. This suggests that more recent books in the dataset are generally well-received by readers, with consistently strong ratings.

Summary

These aggregations demonstrate MongoDB’s ability to efficiently analyze semi-structured data using the aggregation framework. By combining filtering, grouping, and averaging operations, meaningful insights were derived from the book catalog dataset.
