# Diligent Hiring Assignment – E-Commerce Data Pipeline (Completed in Cursor IDE)

This project was built as part of the Diligent hiring challenge.
The goal was simple but meaningful: generate synthetic e-commerce data, ingest it into an SQLite database, and run a multi-table SQL query that returns useful insights.

I completed the entire workflow inside Cursor IDE, using a mix of Python, SQL, and AI-assisted development — but all the logic, structure, and decisions behind the project were made thoughtfully and intentionally.

##  What This Project Does

### 1. Synthetic Data Generation

I created realistic e-commerce datasets representing:

- Customers
- Products
- Orders
- Order Items
- Reviews

The data includes:

- Names, categories, prices
- Order timelines
- Customer purchase patterns
- Product reviews with ratings

All CSVs are stored neatly inside the `data/` folder.

### 2. Database Ingestion (SQLite)

Using `ingest_to_database.py`, I built a small relational database (`ecommerce.db`) with clean schemas and foreign keys:

- `customers`
- `products`
- `orders`
- `order_items`
- `reviews`

The script:

- Creates tables
- Enables foreign key integrity
- Loads all CSVs in the correct order
- Prints progress and status messages

This ensures the database is structured, consistent, and ready for querying.

### 3. Multi-Table SQL Join Query

The script `query_orders.py` performs a meaningful SQL join across five tables.
It retrieves a clear report showing:

- Customer name
- Order date
- Product name
- Quantity
- Unit price
- Average review rating
- Review count

It also:

- Filters orders from the last 90 days
- Computes averages
- Uses LEFT JOIN to include products without reviews
- Outputs a neatly formatted table to `output.txt`

This demonstrates an understanding of relational data and analytical joins.

##  Project Structure

```
DILIGENT_TASK/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── reviews.csv
│
├── ingest_to_database.py
├── generate_ecommerce_data.py
├── query_orders.py
├── output.txt
├── README.md
└── ecommerce.db  (optional)
```

##  How to Run the Project

### 1. Install requirements
```bash
pip install pandas
```

### 2. Re-create the database (optional)
```bash
python ingest_to_database.py
```

### 3. Run the query and view results
```bash
python query_orders.py
```

Check `output.txt` to see the final formatted report.

## A Note From Me

This assignment wasn't just a task — it was a chance to show how I think, how I structure problems, and how I build clean, reliable systems.
I chose to keep the project simple, readable, and practical, while still adding thoughtful touches like:

- Foreign key validation
- Clear data modeling
- Clean formatting
- Organized folder structure

Thank you for reviewing my submission. I hope it reflects the clarity, care, and dedication I bring to every piece of work.

