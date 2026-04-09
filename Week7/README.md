# Week 7 - Pagination Testing with 1 Million Records

This project tests the performance of standard pagination (using `OFFSET` and `LIMIT`) when working with a very large table of 1 million records in an SQLite database using Python and Flask.

## How to run

1. **Install dependencies**
   Make sure you are working in your virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

2. **Seed the database**
   Run the seeding script to generate a `database.db` file with 1M items.
   ```bash
   python seed.py
   ```
   *Note: This could take a few seconds.*

3. **Run the Flask server**
   ```bash
   python app.py
   ```

4. **Test pagination performance**
   The endpoint `/api/records?page=<num>&limit=<num>` will return data along with the time it took to query (`query_time_ms`).

   Test page 1:
   ```bash
   curl "http://localhost:5000/api/records?page=1&limit=10"
   ```

   Test page 90,000 (offset of 900,000 items):
   ```bash
   curl "http://localhost:5000/api/records?page=90000&limit=10"
   ```
   *Notice how the query_time_ms parameter increases as the offset grows.*
