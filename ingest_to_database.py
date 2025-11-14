import sqlite3
import csv
import os
from datetime import datetime

def create_database_schema(conn):
    """Create all tables with proper schema, primary keys, and foreign keys."""
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            signup_date DATE NOT NULL
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    # Create reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            review_text TEXT,
            review_date DATE NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    conn.commit()
    print("Database schema created successfully.")

def load_csv_to_table(conn, csv_file, table_name, columns):
    """Load data from CSV file into database table."""
    cursor = conn.cursor()
    
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found. Skipping...")
        return 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows_inserted = 0
        
        for row in reader:
            # Prepare values in the correct order
            values = [row[col] for col in columns]
            placeholders = ','.join(['?' for _ in columns])
            column_names = ','.join(columns)
            
            try:
                cursor.execute(f'''
                    INSERT INTO {table_name} ({column_names})
                    VALUES ({placeholders})
                ''', values)
                rows_inserted += 1
            except sqlite3.IntegrityError as e:
                print(f"Error inserting row into {table_name}: {e}")
                print(f"Row data: {row}")
            except Exception as e:
                print(f"Unexpected error inserting row into {table_name}: {e}")
                print(f"Row data: {row}")
    
    conn.commit()
    print(f"Loaded {rows_inserted} rows into {table_name} from {csv_file}")
    return rows_inserted

def main():
    # Database file name
    db_file = 'ecommerce.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing {db_file}")
    
    # Create connection
    conn = sqlite3.connect(db_file)
    
    # Enable foreign key constraints
    conn.execute('PRAGMA foreign_keys = ON')
    
    try:
        # Create schema
        create_database_schema(conn)
        
        # Load data from CSV files in correct order (respecting foreign key dependencies)
        print("\nLoading data from CSV files...")
        
        # 1. Load customers first (no dependencies)
        load_csv_to_table(conn, 'customers.csv', 'customers', 
                         ['customer_id', 'name', 'email', 'signup_date'])
        
        # 2. Load products (no dependencies)
        load_csv_to_table(conn, 'products.csv', 'products', 
                         ['product_id', 'name', 'category', 'price'])
        
        # 3. Load orders (depends on customers)
        load_csv_to_table(conn, 'orders.csv', 'orders', 
                         ['order_id', 'customer_id', 'order_date', 'total_amount'])
        
        # 4. Load order_items (depends on orders and products)
        load_csv_to_table(conn, 'order_items.csv', 'order_items', 
                         ['order_item_id', 'order_id', 'product_id', 'quantity', 'price'])
        
        # 5. Load reviews (depends on products and customers)
        load_csv_to_table(conn, 'reviews.csv', 'reviews', 
                         ['review_id', 'product_id', 'customer_id', 'rating', 'review_text', 'review_date'])
        
        # Verify data loaded
        cursor = conn.cursor()
        print("\n" + "="*50)
        print("Data Summary:")
        print("="*50)
        for table in ['customers', 'products', 'orders', 'order_items', 'reviews']:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"{table}: {count} rows")
        
        print("\n" + "="*50)
        print(f"Database '{db_file}' created and populated successfully!")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()


